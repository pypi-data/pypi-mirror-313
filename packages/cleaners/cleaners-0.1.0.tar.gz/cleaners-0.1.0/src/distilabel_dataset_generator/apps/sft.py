import ast
import uuid
from typing import Dict, List, Union

import argilla as rg
import gradio as gr
import pandas as pd
from datasets import Dataset
from distilabel.distiset import Distiset
from huggingface_hub import HfApi

from distilabel_dataset_generator.apps.base import (
    hide_success_message,
    show_success_message,
    validate_argilla_user_workspace_dataset,
    validate_push_to_hub,
)
from distilabel_dataset_generator.constants import DEFAULT_BATCH_SIZE, SFT_AVAILABLE
from distilabel_dataset_generator.pipelines.embeddings import (
    get_embeddings,
    get_sentence_embedding_dimensions,
)
from distilabel_dataset_generator.pipelines.sft import (
    DEFAULT_DATASET_DESCRIPTIONS,
    generate_pipeline_code,
    get_magpie_generator,
    get_prompt_generator,
    get_response_generator,
)
from distilabel_dataset_generator.utils import (
    _LOGGED_OUT_CSS,
    get_argilla_client,
    get_org_dropdown,
    swap_visibility,
)


def convert_dataframe_messages(dataframe: pd.DataFrame) -> pd.DataFrame:
    def convert_to_list_of_dicts(messages: str) -> List[Dict[str, str]]:
        return ast.literal_eval(
            messages.replace("'user'}", "'user'},")
            .replace("'system'}", "'system'},")
            .replace("'assistant'}", "'assistant'},")
        )

    if "messages" in dataframe.columns:
        dataframe["messages"] = dataframe["messages"].apply(
            lambda x: convert_to_list_of_dicts(x) if isinstance(x, str) else x
        )
    return dataframe


def generate_system_prompt(dataset_description, temperature, progress=gr.Progress()):
    progress(0.0, desc="Generating system prompt")
    progress(0.3, desc="Initializing text generation")
    generate_description = get_prompt_generator(temperature)
    progress(0.7, desc="Generating system prompt")
    result = next(
        generate_description.process(
            [
                {
                    "instruction": dataset_description,
                }
            ]
        )
    )[0]["generation"]
    progress(1.0, desc="System prompt generated")
    return result


def generate_sample_dataset(system_prompt, num_turns, progress=gr.Progress()):
    dataframe = generate_dataset(
        system_prompt=system_prompt,
        num_turns=num_turns,
        num_rows=10,
        progress=progress,
        is_sample=True,
    )
    return dataframe


def generate_dataset(
    system_prompt: str,
    num_turns: int = 1,
    num_rows: int = 10,
    is_sample: bool = False,
    progress=gr.Progress(),
) -> pd.DataFrame:
    progress(0.0, desc="(1/2) Generating instructions")
    magpie_generator = get_magpie_generator(system_prompt, num_turns, is_sample)
    response_generator = get_response_generator(system_prompt, num_turns, is_sample)
    total_steps: int = num_rows * 2
    batch_size = DEFAULT_BATCH_SIZE

    # create instructions
    n_processed = 0
    magpie_results = []
    while n_processed < num_rows:
        progress(
            0.5 * n_processed / num_rows,
            total=total_steps,
            desc="(1/2) Generating instructions",
        )
        remaining_rows = num_rows - n_processed
        batch_size = min(batch_size, remaining_rows)
        inputs = [{"system_prompt": system_prompt} for _ in range(batch_size)]
        batch = list(magpie_generator.process(inputs=inputs))
        magpie_results.extend(batch[0])
        n_processed += batch_size
    progress(0.5, desc="(1/2) Generating instructions")

    # generate responses
    n_processed = 0
    response_results = []
    if num_turns == 1:
        while n_processed < num_rows:
            progress(
                0.5 + 0.5 * n_processed / num_rows,
                total=total_steps,
                desc="(2/2) Generating responses",
            )
            batch = magpie_results[n_processed : n_processed + batch_size]
            responses = list(response_generator.process(inputs=batch))
            response_results.extend(responses[0])
            n_processed += batch_size
        for result in response_results:
            result["prompt"] = result["instruction"]
            result["completion"] = result["generation"]
            result["system_prompt"] = system_prompt
    else:
        for result in magpie_results:
            result["conversation"].insert(
                0, {"role": "system", "content": system_prompt}
            )
            result["messages"] = result["conversation"]
        while n_processed < num_rows:
            progress(
                0.5 + 0.5 * n_processed / num_rows,
                total=total_steps,
                desc="(2/2) Generating responses",
            )
            batch = magpie_results[n_processed : n_processed + batch_size]
            responses = list(response_generator.process(inputs=batch))
            response_results.extend(responses[0])
            n_processed += batch_size
        for result in response_results:
            result["messages"].append(
                {"role": "assistant", "content": result["generation"]}
            )
    progress(
        1,
        total=total_steps,
        desc="(2/2) Creating dataset",
    )

    # create distiset
    distiset_results = []
    for result in response_results:
        record = {}
        for relevant_keys in [
            "messages",
            "prompt",
            "completion",
            "model_name",
            "system_prompt",
        ]:
            if relevant_keys in result:
                record[relevant_keys] = result[relevant_keys]
        distiset_results.append(record)

    distiset = Distiset(
        {
            "default": Dataset.from_list(distiset_results),
        }
    )

    # If not pushing to hub generate the dataset directly
    distiset = distiset["default"]
    if num_turns == 1:
        outputs = distiset.to_pandas()[["prompt", "completion", "system_prompt"]]
    else:
        outputs = distiset.to_pandas()[["messages"]]
    dataframe = pd.DataFrame(outputs)
    progress(1.0, desc="Dataset generation completed")
    return dataframe


def push_dataset_to_hub(dataframe, org_name, repo_name, oauth_token, private):
    repo_id = validate_push_to_hub(org_name, repo_name)
    original_dataframe = dataframe.copy(deep=True)
    dataframe = convert_dataframe_messages(dataframe)
    distiset = Distiset({"default": Dataset.from_pandas(dataframe)})
    distiset.push_to_hub(
        repo_id=repo_id,
        private=private,
        include_script=False,
        token=oauth_token.token,
        create_pr=False,
    )
    return original_dataframe


def push_dataset(
    org_name: str,
    repo_name: str,
    system_prompt: str,
    num_turns: int = 1,
    num_rows: int = 10,
    private: bool = False,
    oauth_token: Union[gr.OAuthToken, None] = None,
    progress=gr.Progress(),
) -> pd.DataFrame:
    dataframe = generate_dataset(
        system_prompt=system_prompt,
        num_turns=num_turns,
        num_rows=num_rows,
    )
    push_dataset_to_hub(dataframe, org_name, repo_name, oauth_token, private)
    try:
        progress(0.1, desc="Setting up user and workspace")
        hf_user = HfApi().whoami(token=oauth_token.token)["name"]
        client = get_argilla_client()
        if client is None:
            return ""
        if "messages" in dataframe.columns:
            settings = rg.Settings(
                fields=[
                    rg.ChatField(
                        name="messages",
                        description="The messages in the conversation",
                        title="Messages",
                    ),
                ],
                questions=[
                    rg.RatingQuestion(
                        name="rating",
                        title="Rating",
                        description="The rating of the conversation",
                        values=list(range(1, 6)),
                    ),
                ],
                metadata=[
                    rg.IntegerMetadataProperty(
                        name="user_message_length", title="User Message Length"
                    ),
                    rg.IntegerMetadataProperty(
                        name="assistant_message_length",
                        title="Assistant Message Length",
                    ),
                ],
                vectors=[
                    rg.VectorField(
                        name="messages_embeddings",
                        dimensions=get_sentence_embedding_dimensions(),
                    )
                ],
                guidelines="Please review the conversation and provide a score for the assistant's response.",
            )

            dataframe["user_message_length"] = dataframe["messages"].apply(
                lambda x: sum([len(y["content"]) for y in x if y["role"] == "user"])
            )
            dataframe["assistant_message_length"] = dataframe["messages"].apply(
                lambda x: sum(
                    [len(y["content"]) for y in x if y["role"] == "assistant"]
                )
            )
            dataframe["messages_embeddings"] = get_embeddings(
                dataframe["messages"].apply(
                    lambda x: " ".join([y["content"] for y in x])
                )
            )
        else:
            settings = rg.Settings(
                fields=[
                    rg.TextField(
                        name="system_prompt",
                        title="System Prompt",
                        description="The system prompt used for the conversation",
                        required=False,
                    ),
                    rg.TextField(
                        name="prompt",
                        title="Prompt",
                        description="The prompt used for the conversation",
                    ),
                    rg.TextField(
                        name="completion",
                        title="Completion",
                        description="The completion from the assistant",
                    ),
                ],
                questions=[
                    rg.RatingQuestion(
                        name="rating",
                        title="Rating",
                        description="The rating of the conversation",
                        values=list(range(1, 6)),
                    ),
                ],
                metadata=[
                    rg.IntegerMetadataProperty(
                        name="prompt_length", title="Prompt Length"
                    ),
                    rg.IntegerMetadataProperty(
                        name="completion_length", title="Completion Length"
                    ),
                ],
                vectors=[
                    rg.VectorField(
                        name="prompt_embeddings",
                        dimensions=get_sentence_embedding_dimensions(),
                    )
                ],
                guidelines="Please review the conversation and correct the prompt and completion where needed.",
            )
            dataframe["prompt_length"] = dataframe["prompt"].apply(len)
            dataframe["completion_length"] = dataframe["completion"].apply(len)
            dataframe["prompt_embeddings"] = get_embeddings(dataframe["prompt"])

        progress(0.5, desc="Creating dataset")
        rg_dataset = client.datasets(name=repo_name, workspace=hf_user)
        if rg_dataset is None:
            rg_dataset = rg.Dataset(
                name=repo_name,
                workspace=hf_user,
                settings=settings,
                client=client,
            )
            rg_dataset = rg_dataset.create()
        progress(0.7, desc="Pushing dataset to Argilla")
        hf_dataset = Dataset.from_pandas(dataframe)
        rg_dataset.records.log(records=hf_dataset)
        progress(1.0, desc="Dataset pushed to Argilla")
    except Exception as e:
        raise gr.Error(f"Error pushing dataset to Argilla: {e}")
    return ""


def show_pipeline_code_visibility():
    return {pipeline_code_ui: gr.Accordion(visible=True)}


def hide_pipeline_code_visibility():
    return {pipeline_code_ui: gr.Accordion(visible=False)}


######################
# Gradio UI
######################


with gr.Blocks(css=_LOGGED_OUT_CSS) as app:
    with gr.Column() as main_ui:
        if not SFT_AVAILABLE:
            gr.Markdown(
                value=f"## Supervised Fine-Tuning is not available for the {MODEL} model. Use Hugging Face Llama3 or Qwen2 models."
            )
        else:
            gr.Markdown(value="## 1. Describe the dataset you want")
            with gr.Row():
                with gr.Column(scale=2):
                    dataset_description = gr.Textbox(
                        label="Dataset description",
                        placeholder="Give a precise description of your desired dataset.",
                    )
                    with gr.Accordion("Temperature", open=False):
                        temperature = gr.Slider(
                            minimum=0.1,
                            maximum=1,
                            value=0.8,
                            step=0.1,
                            interactive=True,
                            show_label=False,
                        )
                    load_btn = gr.Button(
                        "Create dataset",
                        variant="primary",
                    )
                with gr.Column(scale=2):
                    examples = gr.Examples(
                        examples=DEFAULT_DATASET_DESCRIPTIONS,
                        inputs=[dataset_description],
                        cache_examples=False,
                        label="Examples",
                    )
                with gr.Column(scale=1):
                    pass

            gr.HTML(value="<hr>")
            gr.Markdown(value="## 2. Configure your dataset")
            with gr.Row(equal_height=False):
                with gr.Column(scale=2):
                    system_prompt = gr.Textbox(
                        label="System prompt",
                        placeholder="You are a helpful assistant.",
                    )
                    num_turns = gr.Number(
                        value=1,
                        label="Number of turns in the conversation",
                        minimum=1,
                        maximum=4,
                        step=1,
                        interactive=True,
                        info="Choose between 1 (single turn with 'instruction-response' columns) and 2-4 (multi-turn conversation with a 'messages' column).",
                    )
                    btn_apply_to_sample_dataset = gr.Button(
                        "Refresh dataset", variant="secondary"
                    )
                with gr.Column(scale=3):
                    dataframe = gr.Dataframe(
                        headers=["prompt", "completion"],
                        wrap=True,
                        height=500,
                        interactive=False,
                    )

            gr.HTML(value="<hr>")
            gr.Markdown(value="## 3. Generate your dataset")
            with gr.Row(equal_height=False):
                with gr.Column(scale=2):
                    org_name = get_org_dropdown()
                    repo_name = gr.Textbox(
                        label="Repo name",
                        placeholder="dataset_name",
                        value=f"my-distiset-{str(uuid.uuid4())[:8]}",
                        interactive=True,
                    )
                    num_rows = gr.Number(
                        label="Number of rows",
                        value=10,
                        interactive=True,
                        scale=1,
                    )
                    private = gr.Checkbox(
                        label="Private dataset",
                        value=False,
                        interactive=True,
                        scale=1,
                    )
                    btn_push_to_hub = gr.Button(
                        "Push to Hub", variant="primary", scale=2
                    )
                with gr.Column(scale=3):
                    success_message = gr.Markdown(visible=True)
                    with gr.Accordion(
                        "Do you want to go further? Customize and run with Distilabel",
                        open=False,
                        visible=False,
                    ) as pipeline_code_ui:
                        code = generate_pipeline_code(
                            system_prompt=system_prompt.value,
                            num_turns=num_turns.value,
                            num_rows=num_rows.value,
                        )
                        pipeline_code = gr.Code(
                            value=code,
                            language="python",
                            label="Distilabel Pipeline Code",
                        )

        load_btn.click(
            fn=generate_system_prompt,
            inputs=[dataset_description, temperature],
            outputs=[system_prompt],
            show_progress=True,
        ).then(
            fn=generate_sample_dataset,
            inputs=[system_prompt, num_turns],
            outputs=[dataframe],
            show_progress=True,
        )

        btn_apply_to_sample_dataset.click(
            fn=generate_sample_dataset,
            inputs=[system_prompt, num_turns],
            outputs=[dataframe],
            show_progress=True,
        )

        btn_push_to_hub.click(
            fn=validate_argilla_user_workspace_dataset,
            inputs=[repo_name],
            outputs=[success_message],
            show_progress=True,
        ).then(
            fn=validate_push_to_hub,
            inputs=[org_name, repo_name],
            outputs=[success_message],
            show_progress=True,
        ).success(
            fn=hide_success_message,
            outputs=[success_message],
            show_progress=True,
        ).success(
            fn=hide_pipeline_code_visibility,
            inputs=[],
            outputs=[pipeline_code_ui],
        ).success(
            fn=push_dataset,
            inputs=[
                org_name,
                repo_name,
                system_prompt,
                num_turns,
                num_rows,
                private,
            ],
            outputs=[success_message],
            show_progress=True,
        ).success(
            fn=show_success_message,
            inputs=[org_name, repo_name],
            outputs=[success_message],
        ).success(
            fn=generate_pipeline_code,
            inputs=[system_prompt, num_turns, num_rows],
            outputs=[pipeline_code],
        ).success(
            fn=show_pipeline_code_visibility,
            inputs=[],
            outputs=[pipeline_code_ui],
        )

        app.load(fn=swap_visibility, outputs=main_ui)
        app.load(fn=get_org_dropdown, outputs=[org_name])
