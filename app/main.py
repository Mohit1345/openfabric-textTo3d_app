import logging
from typing import Dict

from utils.filehandle import save_image, save_model
from utils.llmCall import call_llm_generate  
from utils.memory_manager import MemoryManager
from utils.vectordb import VectorMemoryManager
from ontology_dc8f06af066e4a7880a5938933236037.config import ConfigClass
from ontology_dc8f06af066e4a7880a5938933236037.input import InputClass
from ontology_dc8f06af066e4a7880a5938933236037.output import OutputClass
from openfabric_pysdk.context import AppModel, State
from core.stub import Stub

from datetime import datetime
import logging

# Configurations for the app
configurations: Dict[str, ConfigClass] = dict()

############################################################
# Config callback function
############################################################
def config(configuration: Dict[str, ConfigClass], state: State) -> None:
    """
    Stores user-specific configuration data.

    Args:
        configuration (Dict[str, ConfigClass]): A mapping of user IDs to configuration objects.
        state (State): The current state of the application (not used in this implementation).
    """
    for uid, conf in configuration.items():
        logging.info(f"Saving new config for user with id:'{uid}'")
        configurations[uid] = conf


############################################################
# Execution callback function
############################################################
# def execute(model: AppModel) -> None:
#     """
#     Main execution entry point for handling a model pass.

#     Args:
#         model (AppModel): The model object containing request and response structures.
#     """

#     # Retrieve input
#     request: InputClass = model.request

#     # Retrieve user config
#     user_config: ConfigClass = configurations.get('super-user', None)
#     logging.info(f"{configurations}")

#     # Initialize the Stub with app IDs
#     app_ids = user_config.app_ids if user_config else []
#     stub = Stub(app_ids)

#     # ------------------------------
#     # TODO : add your magic here
#     # ------------------------------



#     # Prepare response
#     response: OutputClass = model.response
#     response.message = f"Echo: {request.prompt}"


# main.py


# Assuming your constants:
TEXT2IMG_APP_ID = 'c25dcd829d134ea98f5ae4dd311d13bc.node3.openfabric.network'
IMG2_3D_APP_ID = '69543f294d414afc7f293d51591f11eb.node3.openfabric.network'

def execute(model: AppModel) -> None:
    print("Incoming request:", model)
    request: InputClass = model.request
    response: OutputClass = model.response

    user_config: ConfigClass = configurations.get('super-user', None)
    logging.info(f"Current configurations: {user_config}")
    app_ids = user_config.app_ids if user_config else []
    stub = Stub(app_ids)

    vector_memory = VectorMemoryManager()
    memory_manager = MemoryManager()

    # Step 1️⃣: Prompt Construction
    original_prompt = request.prompt or ""
    short_term_prompts = "\n".join(
        f"{i+1}. {st['original_prompt']} → {st['expanded_prompt']}"
        for i, st in enumerate(memory_manager.short_term_memory)
    )
    original_prompt += (
        "\n\nYou are an expert prompt engineer who writes creative prompts "
        "without any extra questions or information. These prompts are used "
        "to generate images or 3D models, such as objects or game characters. "
        "Refer to the Short Term Memory Prompts below if needed:\n" + short_term_prompts
    )

    expanded_prompt = original_prompt  # fallback

    if request.ai_enhaned:
        logging.info("🔍 Calling LLM to enhance prompt")
        expanded_prompt = call_llm_generate(0, original_prompt)

    if request.recallLongTermMemory:
        logging.info("🔁 Recalling from long term memory")
        similar_prompts = vector_memory.search_similar(original_prompt, top_k=3)
        logging.info(f"Found {len(similar_prompts)} similar prompts in long term memory")
        if len(similar_prompts)>0:
            expanded_prompt += "\n\nSimilar Prompts:\n" + "\n".join(
                f"{i+1}. {sp['prompt']}" for i, sp in enumerate(similar_prompts)
            )

    logging.info(f"📝 Final Prompt: {expanded_prompt}")

    # Step 2️⃣: Text to Image
    try:
        text2img_response = stub.call(TEXT2IMG_APP_ID, {'prompt': expanded_prompt}, 'super-user')
        image_data = text2img_response.get('result')
        image_path = save_image(image_data)
        logging.info(f"🖼️ Image saved at: {image_path}")
    except Exception as e:
        logging.exception("❌ Error in text-to-image step")
        response.message = f"Error in text-to-image step: {str(e)}"
        response.image_path = None
        response.model_path = None
        response.session_id = request.session_id
        return

    
    memory_manager.append_short_term({
            'original_prompt': original_prompt,
            'expanded_prompt': expanded_prompt,
            'image_path': image_path,
            'timestamp': datetime.utcnow().isoformat()
        })

    memory_manager.save_to_long_term()

    # Step 3️⃣: Image to 3D
    # APP ID not found , once found , set it above on IMG2_3D_APP_ID,  just needed to uncomment below code 
    # try:
    #     img2model_response = stub.call(IMG2_3D_APP_ID, {'image': image_data}, 'super-user')
    #     model_data = img2model_response.get('result')
    #     model_path = save_model(model_data)
    #     logging.info(f"📦 3D model saved at: {model_path}")
    # except Exception as e:
    #     logging.exception("❌ Error in image-to-3D step")
    #     response.message = f"Error in image-to-3D step: {str(e)}"
    #     response.image_path = image_path
    #     response.model_path = None
    #     response.session_id = request.session_id
    #     return

    # Step 4️⃣: Save Vector db
    vector_memory.add_prompt(original_prompt, meta={
        'image_path': image_path,
        # 'model_path': model_path,
        'timestamp': datetime.utcnow().isoformat()
    })
    # Final Response
    response.message = "✨ Success! Generated image and 3D model."
    response.image_path = image_path
    response.model_path = ""
    response.session_id = request.session_id
