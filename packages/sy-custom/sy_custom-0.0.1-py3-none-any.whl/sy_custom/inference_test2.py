import torch
from diffusers import FlowMatchEulerDiscreteScheduler, AutoencoderKL
from diffusers.models.transformers.transformer_flux import FluxTransformer2DModel
from diffusers.pipelines.flux.pipeline_flux import FluxPipeline
from transformers import CLIPTextModel, CLIPTokenizer,T5EncoderModel, T5TokenizerFast
from library import flux_models, flux_utils
import os
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
transformer = FluxTransformer2DModel.from_single_file("./newgrille_viewterms_metadata_1202_epoch100/flux_carcon.safetensors",torch_dtype=dtype)

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
                         ],
                   19: ["hyundai_ioniq-5_2024, front view, genesis_g70_2019 grille",
                        "hyundai_ioniq-5_2024, front view, round headlight",
                        "genesis_g70_2019, front view, kidney grille"],
                  20:["hyundai_ioniq-5_2024, front view",
                      "hyundai_ioniq-5_2024, rear view",
                      "hyundai_ioniq-5_2024, rear three-quarter view", "hyundai_ioniq-5_2024, front three-quarter view"],
                  21: ["hyundai_ioniq-5_2024, front view, the headlights design is round and circle",
                        "A front-view of hyundai_ioniq-5_2024",
                        "hyundai_ioniq-5_2024, rear three-quarter view"]}

########################################################

car_prompt_list_new = {0:["car model: hyundai_ioniq-5_2024",
                      "car model: hyundai_ioniq-5_2024, view: front three-quarter view",
                      "car model: hyundai_ioniq-5_2024, view: front three-quarter view, description: Its design language is undeniably modern and minimalist, with clean lines and a sharp silhouette, The profile exhibits sleek and flattened character lines that create a dynamic sense of movement even while stationary, One prominent feature is the integration of the DRLs into the headlight assembly that, along with the shape of the light cluster, imparts an innovative and high-tech look to the front facade, Every design detail of the parts listed works in concert to create a harmonious and refined exterior aesthetic."],
                       1:["hyundai_ioniq-5_2024, front side view", "hyundai_ioniq-5_2024, rear side view"],}

######################################################
car_prompt_list_view = {0:["hyundai_ioniq-5_2024, front side view","hyundai_ioniq-5_2024, front view", "hyundai_ioniq-5_2024, rear side view","hyundai_ioniq-5_2024, rear view","hyundai_ioniq-5_2024, profile view"],
                  1:["Create a high-resolution, professional automotive photograph of a 2024 Hyundai Ioniq 5, showcasing a front-side view. The car should be set against a modern urban backdrop during sunset, with realistic lighting and reflections. Emphasize detailed textures, sharp focus, and vibrant colors to highlight the vehicle's design. Render in 8K resolution for maximum clarity.","Create a high-resolution, professional automotive photograph of a 2024 Hyundai Ioniq 5, showcasing a front view. The car should be set against a modern urban backdrop during sunset, with realistic lighting and reflections. Emphasize detailed textures, sharp focus, and vibrant colors to highlight the vehicle's design. Render in 8K resolution for maximum clarity.","Create a high-resolution, professional automotive photograph of a 2024 Hyundai Ioniq 5, showcasing a rear-side view. The car should be set against a modern urban backdrop during sunset, with realistic lighting and reflections. Emphasize detailed textures, sharp focus, and vibrant colors to highlight the vehicle's design. Render in 8K resolution for maximum clarity.","Create a high-resolution, professional automotive photograph of a 2024 Hyundai Ioniq 5, showcasing a profile view. The car should be set against a modern urban backdrop during sunset, with realistic lighting and reflections. Emphasize detailed textures, sharp focus, and vibrant colors to highlight the vehicle's design. Render in 8K resolution for maximum clarity."]}

##############################################
car_prompt_list_test = {0:["Create an ultra-realistic, high-resolution image of a kia sportage, viewed from the front side view. The car should showcase professional design elements, with detailed textures, realistic lighting, shadows, and reflections."], 
                        1:["Create an ultra-realistic, high-resolution image of a kia sportage with round headlamp,rounded headlamp,circular headlamp,oval headlamp, viewed from the front side view. The car should showcase professional design elements, with detailed textures, realistic lighting, shadows, and reflections."],
                      2:["front side view, Its design language is undeniably modern and minimalist, with clean lines and a sharp silhouette, The profile exhibits sleek and flattened character lines that create a dynamic sense of movement even while stationary, One prominent feature is the integration of the DRLs into the round headlight assembly that, along with the shape of the light cluster, imparts an innovative and high-tech look to the front facade, Every design detail of the parts listed works in concert to create a harmonious and refined exterior aesthetic."],
                        3:["front side view, Its design language is undeniably modern and minimalist, with clean lines and a sharp silhouette, The profile exhibits sleek and flattened character lines that create a dynamic sense of movement even while stationary, One prominent feature is the integration of the DRLs into the round, circular headlight. This shape is achieved by arranging the various components of the headlight-such as the bulb, reflector, and lens-within a circular housing. Surrounding the lens is often a circular bezel or trim"],
                        4:["Create an ultra-realistic, high-resolution image of a sedan car with round/rounded/ circular/oval headlamps, viewed from the front side view.","Create an ultra-realistic, high-resolution image of a sedan car with automobile headlights having outer frames in the shape of a perfect round/rounded/circular/oval, the outer frames are of the headlights having circular shape, viewed from the front side view.","Create an ultra-realistic, high-resolution image of a sedan car with an automobile radiator grille having an outer frame in the shape of a perfect equilateral triangle, the outer frame of the grille having equal sides and angles, and one vertex of the triangle above and two vertices below."],
                        5:["A sleek and modern sedan from the 2010s featuring dual round LED headlights with intricate reflector detailing inside. The car has a streamlined body with subtle creases along the hood and doors, a trapezoidal grille framed with chrome, and a smooth metallic finish in pearl white. The wheels are multi-spoke alloys with low-profile tires. The front bumper integrates aerodynamic air vents and a slim, integrated front splitter. Ultra-detailed rendering of the headlight components and surface textures."],
                        6:["A photorealistic depiction of a car. The car features round LED headlights with black trim, and a body-colored front bumper with integrated air vents. Black side mirrors match the car's contrasting black roof, and the stylish alloy wheels have a modern multi-spoke design. The windows are tinted with black trim, and the front fenders are slightly flared for a sporty look."],
                        7:["front side view, Its design language is undeniably modern and minimalist, with clean lines and a sharp silhouette, The profile exhibits sleek and flattened character lines that create a dynamic sense of movement even while stationary, One prominent feature is the round Headlight assembly.", "front three-quarter view, Its design language is undeniably modern and minimalist, with clean lines and a sharp silhouette, The profile exhibits sleek and flattened character lines that create a dynamic sense of movement even while stationary, One prominent feature is the circle Headlight assembly.","front three-quarter view, Its design language is undeniably modern and minimalist, with clean lines and a sharp silhouette, the profile exhibits sleek and flattened character lines that create a dynamic sense of movement even while stationary, One prominent feature is the circle outer lens."],
                        8:["front side view, Its design language is undeniably modern and minimalist, with clean lines and a sharp silhouette, The profile exhibits sleek and flattened character lines that create a dynamic sense of movement even while stationary, One prominent feature is round headlight housing surrounded a circular bezel or trim.", "Create an ultra-realistic, high-resolution image of sedan car with round headlight housing, viewed from the front side view. The car should showcase professional design elements, with detailed textures, realistic lighting, shadows, and reflections."],
                        9:["A compact and stylish sedan car, featuring perfectly round headlight housings that stand out prominently on the front of the vehicle. The headlights are fully circular with smooth chrome or black trims surrounding them. The car has a sleek and aerodynamic body, a low profile, and a sporty yet elegant look. The front grille complements the round headlights with minimalistic styling. Ensure the round headlights are the most defining feature of the car’s front design."],
                        10:["The car in the image is a luxury grand tourer with a commanding and elegant front design, highlighted by a large, rectangular chrome grille with a diamond-mesh pattern that radiates sophistication. The grille is flanked by dual circular headlights on each side, featuring intricate LED detailing that enhances its premium and modern appeal. The smoothly contoured hood leads into a bold front fascia, giving the car a seamless and aerodynamic look. The lower bumper integrates additional air intakes and subtle accents, contributing to both functionality and a sporty aesthetic. The side mirrors are sleek and painted to match the body color, emphasizing the car's streamlined profile. At the center of the grille, a distinctive emblem symbolizes the brand's heritage and status. The overall design merges traditional luxury with contemporary performance styling, exuding power and exclusivity."],
                        11:["The car in the image is a luxury grand tourer with a commanding and elegant front design, highlighted by a large, triangular chrome grille with a diamond-mesh pattern that radiates sophistication. The grille is flanked by dual circular headlights on each side, featuring intricate LED detailing that enhances its premium and modern appeal. The smoothly contoured hood leads into a bold front fascia, giving the car a seamless and aerodynamic look. The lower bumper integrates additional air intakes and subtle accents, contributing to both functionality and a sporty aesthetic. The side mirrors are sleek and painted to match the body color, emphasizing the car's streamlined profile. At the center of the grille, a distinctive emblem symbolizes the brand's heritage and status. The overall design merges traditional luxury with contemporary performance styling, exuding power and exclusivity."],
                        12:["The car in the image is a luxury grand tourer with a commanding and elegant front design, marked by its distinctive reverse triangular grille with horizontal chrome slats, which emphasizes a modern and dynamic character. The grille is flanked by dual circular headlights on each side, featuring intricate LED detailing that enhances its premium and modern appeal. The smoothly contoured hood leads into a bold front fascia, giving the car a seamless and aerodynamic look. The lower bumper integrates additional air intakes and subtle accents, contributing to both functionality and a sporty aesthetic. The side mirrors are sleek and painted to match the body color, emphasizing the car's streamlined profile. At the center of the grille, a distinctive emblem symbolizes the brand's heritage and status. The overall design merges traditional luxury with contemporary performance styling, exuding power and exclusivity."],
                        13:["The car in the image features a bold and unconventional design, marked by its distinctive reverse triangular grille with horizontal chrome slats, which emphasizes a modern and dynamic character. At the center of the grille, a circular emblem reinforces the vehicle's brand identity, serving as a focal point. The sharply contoured hood, with prominent ridges, adds a sense of muscularity and motion to the overall design. The angular headlights, positioned on either side of the grille, have a sweeping shape that flows seamlessly into the car's front profile, enhancing its aerodynamic appeal. The lower bumper incorporates circular fog lights set in blacked-out surrounds, providing both functional lighting and a sporty accent. The vibrant blue body color is complemented by body-colored side mirrors and subtle wheel arches, which together give the car a cohesive and confident stance. This design combines futuristic styling with bold aesthetics, making it stand out on the road."],
                        14:["The car in the image features a bold and unconventional design, marked by its distinctive upright triangular grille with horizontal chrome slats, which emphasizes a modern and dynamic character. At the center of the grille, a circular emblem reinforces the vehicle's brand identity, serving as a focal point. The sharply contoured hood, with prominent ridges, adds a sense of muscularity and motion to the overall design. The angular headlights, positioned on either side of the grille, have a sweeping shape that flows seamlessly into the car's front profile, enhancing its aerodynamic appeal. The lower bumper incorporates circular fog lights set in blacked-out surrounds, providing both functional lighting and a sporty accent. The vibrant blue body color is complemented by body-colored side mirrors and subtle wheel arches, which together give the car a cohesive and confident stance. This design combines futuristic styling with bold aesthetics, making it stand out on the road."],
                        15:["The blue car in the image is a luxury grand tourer with a commanding and elegant front design, highlighted by a large, rectangular chrome grille with a diamond-mesh pattern that radiates sophistication. The grille is flanked by dual circular headlights on each side, featuring intricate LED detailing that enhances its premium and modern appeal. The smoothly contoured hood leads into a bold front fascia, giving the car a seamless and aerodynamic look. The lower bumper integrates additional air intakes and subtle accents, contributing to both functionality and a sporty aesthetic. The side mirrors are sleek and painted to match the body color, emphasizing the car's streamlined profile. At the center of the grille, a distinctive emblem symbolizes the brand's heritage and status. The overall design merges traditional luxury with contemporary performance styling, exuding power and exclusivity.",
                            "The vibrant blue body color car in the image is a luxury grand tourer with a commanding and elegant front design, highlighted by a large, rectangular chrome grille with a diamond-mesh pattern that radiates sophistication. The grille is flanked by dual circular headlights on each side, featuring intricate LED detailing that enhances its premium and modern appeal. The smoothly contoured hood leads into a bold front fascia, giving the car a seamless and aerodynamic look. The lower bumper integrates additional air intakes and subtle accents, contributing to both functionality and a sporty aesthetic. The side mirrors are sleek and painted to match the body color, emphasizing the car's streamlined profile. At the center of the grille, a distinctive emblem symbolizes the brand's heritage and status. The overall design merges traditional luxury with contemporary performance styling, exuding power and exclusivity.",
                            "The car in the image is a luxury grand tourer with a commanding and elegant front design, highlighted by a large, rectangular chrome red grille with a diamond-mesh pattern that radiates sophistication. The red grille is flanked by dual circular yellow headlights on each side, featuring intricate LED detailing that enhances its premium and modern appeal. The smoothly contoured blue hood leads into a bold front fascia, giving the car a seamless and aerodynamic look. The lower green bumper integrates additional air intakes and subtle accents, contributing to both functionality and a sporty aesthetic. The side mirrors are sleek and painted to white color, emphasizing the car's streamlined profile. At the center of the grille, a distinctive emblem symbolizes the brand's heritage and status. The overall design merges traditional luxury with contemporary performance styling, exuding power and exclusivity."], #색상으로 각 파트 인식하는지 확인하기, 예를 들어 파란색그릴,노란색후드, 등
                        16:["The car in the image is a modern compact hatchback with a distinctive and playful design that blends retro aesthetics with contemporary elements. Its front fascia features a rounded grille with a sleek black surround and a subtle badge at the center, maintaining a minimalist yet iconic look. The circular LED headlights, outlined with glowing light rings, contribute to its unique and recognizable character. The body is painted in a soft silver tone, contrasted by a glossy black roof and matching trim elements that add a sporty, dual-tone effect. Bright yellow accents, including the side mirrors and inserts on the aerodynamic wheels, introduce a bold, electric-themed aesthetic, suggesting the vehicle's eco-friendly nature. The car sits low to the ground, with clean, smooth curves and slightly flared wheel arches that enhance its dynamic stance. Overall, the design combines timeless charm with futuristic cues, making it both stylish and forward-thinking."], # 재현목적
                        17:["The car in the image is a luxury grand tourer with a commanding and elegant front design, highlighted by a large, rectangular chrome grille with a diamond-mesh pattern that radiates sophistication. The grille is flanked by V-shaped positioning lamps, and pixelated headlamps on each side, featuring intricate LED detailing that enhances its premium and modern appeal. The smoothly contoured hood leads into a bold front fascia, giving the car a seamless and aerodynamic look. The lower bumper integrates additional air intakes and subtle accents, contributing to both functionality and a sporty aesthetic. The side mirrors are sleek and painted to match the body color, emphasizing the car's streamlined profile. At the center of the grille, a distinctive emblem symbolizes the brand's heritage and status. The overall design merges traditional luxury with contemporary performance styling, exuding power and exclusivity."], #v shaped 
                        18:["The car in the image is a luxury grand tourer with a commanding and elegant front design, highlighted by a large, kidney grille. The kideney grille is flanked by dual circular headlights on each side, featuring intricate LED detailing that enhances its premium and modern appeal. The smoothly contoured hood leads into a bold front fascia, giving the car a seamless and aerodynamic look. The lower bumper integrates additional air intakes and subtle accents, contributing to both functionality and a sporty aesthetic. The side mirrors are sleek and painted to match the body color, emphasizing the car's streamlined profile. At the center of the grille, a distinctive emblem symbolizes the brand's heritage and status. The overall design merges traditional luxury with contemporary performance styling, exuding power and exclusivity."], #kidney grille
                        19:["hyundai_ioniq-5_2024, front side view", "hyundai_ioniq-5_2024, rear side view","hyundai_ioniq-5_2024, lateral view","hyundai_ioniq-5_2024, front view","hyundai_ioniq-5_2024, rear view"], #시점
                        20:["front three-quarter view, This vehicle features a monochromatic color scheme with a bold finish and distinctive V-shaped grille that gives it an aggressive yet elegant look that enhances its sharp and assertive design language, The overall design language of this car is futuristic and dynamic, with a strong and pronounced silhouette, Aesthetically, the vehicle evokes a sense of speed and precision with sculpted lines that flow from the hood to the rear, Each of the individual design components integrates harmoniously to create a cohesive and visually striking vehicle","front three-quarter view, This vehicle features a monochromatic color scheme with a bold finish and the V-shaped grille is characterized by its converging lines that form a sharp, angled design running from the top outward edges down to a central point,that and enhances its sharp and assertive design language, The overall design language of this car is futuristic and dynamic, with a strong and pronounced silhouette, Aesthetically, the vehicle evokes a sense of speed and precision with sculpted lines that flow from the hood to the rear, Each of the individual design components integrates harmoniously to create a cohesive and visually striking vehicle"],
                        21:["The front side view of this sleek modern sedan exudes an aura of aerodynamic efficiency coupled with a dynamic sportive flair. One prominent feature is the round, circular headlights. THis shape is achieved by arranging the various components of the headlight-such as the bulb,reflector and lens-within a circular housing."],
                        22:["round headlamps"]
                        
                      
}




# Settings
#prompt    = "hyundai_ioniq-5_2024, front three-quarter view"
width     = 1024
height    = 1024
guidance  = 3.5
steps     = 28
seed      = 123456

# Generation


#save_folder_ = './inference_output_epoch20/'

for pi,prompt in car_prompt_list_test.items():
    #import pdb; pdb.set_trace()
    if pi not in [22]:
    #if pi not in [20,21]:
        continue
    
    for idx,pro in enumerate(prompt):
        save_folder_tmp =f'./inference_ouput_newgrille_viewterms_metadata/{pi}/{idx}'
        if not os.path.exists(save_folder_tmp):
            os.makedirs(save_folder_tmp)
            
        for i in range(4):
            seed_ = seed + i
            save_imgname = f'{save_folder_tmp}/finetuning_{seed_}.jpg'
            image = pipe(
              prompt=pro,
              width=width,
              height=height,
              guidance_scale=guidance,
              num_inference_steps=steps,
              generator=torch.Generator("cuda").manual_seed(seed_)
            ).images[0]

            image.save(save_imgname)
