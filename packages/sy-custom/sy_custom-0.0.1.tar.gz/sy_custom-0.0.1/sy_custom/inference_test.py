import torch
from diffusers import FlowMatchEulerDiscreteScheduler, AutoencoderKL
from diffusers.models.transformers.transformer_flux import FluxTransformer2DModel
from diffusers.pipelines.flux.pipeline_flux import FluxPipeline
from transformers import CLIPTextModel, CLIPTokenizer,T5EncoderModel, T5TokenizerFast
from library import flux_models, flux_utils
# Model data type
dtype = torch.bfloat16

##############
# LOAD MODEL #
##############

# Local Folders
bfl_dir = "./flux_model/"
tkn_dir = "./flux_model/tokenizer/"

# Load model components
scheduler = FlowMatchEulerDiscreteScheduler.from_pretrained(bfl_dir, subfolder="scheduler", torch_dtype=dtype)

text_encoder= CLIPTextModel.from_pretrained("./flux_model/text_encoder/", torch_dtype=dtype)
tokenizer= CLIPTokenizer.from_pretrained("./flux_model/tokenizer/", torch_dtype=dtype, clean_up_tokenization_spaces=True)

text_encoder_2= T5EncoderModel.from_pretrained(bfl_dir, subfolder="text_encoder_2", torch_dtype=dtype)
tokenizer_2= T5TokenizerFast.from_pretrained(bfl_dir, subfolder="tokenizer_2", torch_dtype=dtype, clean_up_tokenization_spaces=True)
vae = AutoencoderKL.from_pretrained(bfl_dir, subfolder="vae", torch_dtype=dtype)

# Load model
#transformer = FluxTransformer2DModel.from_pretrained(bfl_dir, subfolder="transformer", torch_dtype=dtype)
transformer = FluxTransformer2DModel.from_single_file("./flux_output5/flux_carcon.safetensors",torch_dtype=dtype)

############
# PIPELINE #
############

# Create pipe
pipe = FluxPipeline(
  scheduler=scheduler,
  text_encoder=text_encoder,
  tokenizer=tokenizer,
  text_encoder_2=text_encoder_2,
  tokenizer_2=tokenizer_2,
  vae=vae,
  transformer=transformer
)
pipe.enable_sequential_cpu_offload()
pipe.vae.enable_slicing()
pipe.vae.enable_tiling()

#############
# INFERENCE #
#############
car_prompt_list = {0:["hyundai_ioniq-5_2024",
                      "hyundai_ioniq-5_2024, front three-quarter view",
                      "hyundai_ioniq-5_2024, front three-quarter view, Its design language is undeniably modern and minimalist, with clean lines and a sharp silhouette, The profile exhibits sleek and flattened character lines that create a dynamic sense of movement even while stationary, One prominent feature is the integration of the DRLs into the headlight assembly that, along with the shape of the light cluster, imparts an innovative and high-tech look to the front facade, Every design detail of the parts listed works in concert to create a harmonious and refined exterior aesthetic."],
                  1:["lexus_rz_2023",
                    "lexus_rz_2023,Rear three-quarter view,high-gloss finish",
                    "lexus_rz_2023,Rear three-quarter view,Visually compelling design features such as the sleek integration of the taillights and sharp character lines contribute to a feeling of forward motion even when stationary."],
                    2:["genesis_gv70_2023",
                        "genesis_gv70_2023, front three-quarter view",
                        "genesis_gv70_2023, front three-quarter view, prominent is the expansive grille which gives the front an assertive face, complemented by slim, aggressive headlights and sculptural accents surrounding the drls."],
                    3:["kia_sportage_2023",
                        "kia_sportage_2023, front three-quarter view",
                        "kia_sportage_2023, front three-quarter view, deep lustrous color, The integration of the car parts such as the front fender, headlights, and grille create a harmonious and focused expression that captures the vehicle's athletic character."],
                    4:["genesis_g70_2019",
                        "genesis_g70_2019, side view",
                        "genesis_g70_2019,side view, its silhouette demonstrates a smooth flow from front to rear, punctuated by a fastback-like roof line that slopes gently into the rear deck, suggesting a sporty character. the belt line that stretches from the headlights to the rear lamps and the pronounced rocker panel line add to the dynamic look of the vehicle."],
                    5:["mercedes-benz_amg-gt_2017",
                        "mercedes-benz_amg-gt_2017, side view",
                        "mercedes-benz_amg-gt_2017, The silhouette of the car denotes a grand touring character with smooth, sweeping lines that glide from the front to the back, Design elements such as pronounced wheel arches and the sculpted rocker panel line endorse a dynamic and grounded stance, The design of each part is thoughtfully integrated, resulting in a cohesive and harmonious appearance"],
                    6:["ram_1500_2025",
                        "ram_1500_2025, rear three-quarter",
                        "ram_1500_2025, substantial rear cargo area and a solid, muscular stance. the inherently boxy shape is moderated by some subtle curves and line work that adds dynamism to its appearance."],
                    7:["hyundai_ioniq-5_2024, side view",
                        "hyundai_ioniq-5_2024, side view, vibrant red for the body",
                        "hyundai_ioniq-5_2024, side view,The black color and glossy finish exude sophistication"],
                    8:["mercedes-benz_amg-gt_2017, front three-quarter view",
                        "mercedes-benz_amg-gt_2017, front three-quarter view, vibrant red for the body",
                        "mercedes-benz_amg-gt_2017, front three-quarter view, vibrant yellow for the body"],
                    9:["kia_sportage_2023, front three-quarter view, suggested by a broad grille and the aggressive contours of the front bumper",
                        "kia_sportage_2023, front three-quarter view,the large, commanding grille takes center stage, flanked by the headlights that sharpen the vehicle's face and add to the determined look.",
                        "kia_sportage_2023, front three-quarter view,the expansive grille provides a bold front fascia that is both striking and intricate, asserting the vehicle's road presence. large, sculpted headlights augment the vehicle's assertive look and are seamlessly integrated into the design."],
                    10:["hyundai_ioniq-5_2024",
                        "hyundai_ioniq-5_2024, car",
                        "hyundai_ioniq-5_2024, suv"],
                   11:["lexus_rz_2023",
                        "lexus_rz_2023, car",
                        "lexus_rz_2023, suv"],
                   12:["genesis_gv70_2023",
                        "genesis_gv70_2023, car",
                        "genesis_gv70_2023, suv"],
                   13:["kia_sportage_2023",
                        "kia_sportage_2023, car",
                        "kia_sportage_2023, suv"],
                   14:["genesis_g70_2019",
                        "genesis_g70_2019, car",
                        "genesis_g70_2019, sedan"],
                   15:["mercedes-benz_amg-gt_2017",
                        "mercedes-benz_amg-gt_2017, car",
                        "mercedes-benz_amg-gt_2017, sedan"],
                   16:['ram_1500_2025','ram_1500_2025, car', 'ram_1500_2025, truck'],
                   17:['genesis_g70_2019','genesis_g70_2019, hyundai genesis','genesis_g70_2019, car, hyundai genesis',],
                     18: ['SUV looks like genesis_gv70_2019 and kia_sportage_2023, concept, front three-quarter view',
                          'SUV looks like kia_sportage_2023 and genesis_gv70_2019, concept, front three-quarter view',
                         'SUV looks like genesis gv70 and kia sportage, genesis_gv70, kia_sportage_2023, concept, front three-quarter view',
                         ],}

# Settings
prompt    = "hyundai_ioniq-5_2024, front three-quarter view"
width     = 1024
height    = 1024
guidance  = 3.5
steps     = 28
seed      = 123456

# Generation
image = pipe(
  prompt=prompt,
  width=width,
  height=height,
  guidance_scale=guidance,
  num_inference_steps=steps,
  generator=torch.Generator("cuda").manual_seed(seed)
).images[0]
image.save("./inference_output/image5.png")