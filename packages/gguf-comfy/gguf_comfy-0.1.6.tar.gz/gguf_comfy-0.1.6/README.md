### ComfyUI GGUF

custom node diagram generator (image/audio/video)

#### download the portal via
```
py -m gguf_comfy
```

![screenshot](https://raw.githubusercontent.com/calcuis/gguf-comfy/master/gguf.png)

- decompress the 7z bundle file: Extract All... (it includes everything you need to run a model)
- you could either get the dry run pack [here](https://huggingface.co/calcuis/flux1-gguf/tree/main) or pick them one-by-one from the original source below
- download [flux1-dev-Q4_0.gguf](https://huggingface.co/city96/FLUX.1-dev-gguf/blob/main/flux1-dev-Q4_0.gguf) (6.32GB); pull it to ./ComfyUI/models/unet
- download [clip_l.safetensors](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/clip_l.safetensors) (234MB) and [t5xxl_fp8_e4m3fn.safetensors](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp8_e4m3fn.safetensors) (4.55GB); pull them to ./ComfyUI/models/clip
- download [ae.safetensors](https://huggingface.co/black-forest-labs/FLUX.1-schnell/blob/main/ae.safetensors) (319MB); pull it to ./ComfyUI/models/vae
- run the .bat file under the main directory (it will activate the py backend as well as the js frontend)
- drag [gguf-workflow.json](https://github.com/calcuis/gguf-comfy/blob/main/gguf-workflow.json) to the activated browser

You are good to GO! (now you can run flux1 with the cheapest Nvidia GPU or merely CPU) ENJOY!
#### Reference: [flux](https://github.com/black-forest-labs/flux) [comfyanonymous](https://github.com/comfyanonymous/ComfyUI) [city96](https://github.com/city96/ComfyUI-GGUF) 

![screenshot](https://raw.githubusercontent.com/calcuis/comfy/master/sd3.png)
#### Stable Diffusion 3.5 is now supported (please upgrade to the latest version)

Run sd3.x model following the step-by-step guide below:
- you could either get the backup pack [here](https://huggingface.co/calcuis/sd3.5-large-gguf/tree/main) or pick them one-by-one from the original source below
- download [sd3.5_large-q4_0.gguf](https://huggingface.co/calcuis/sd3.5-large-gguf/blob/main/sd3.5_large-q4_0.gguf) (4.77GB); pull it to ./ComfyUI/models/unet
- download [clip_g.safetensors](https://huggingface.co/stabilityai/stable-diffusion-3.5-large/blob/main/text_encoders/clip_g.safetensors) (1.39GB),  [clip_l.safetensors](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/clip_l.safetensors) (234MB), and [t5xxl_fp8_e4m3fn.safetensors](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp8_e4m3fn.safetensors) (4.55GB); pull them all to ./ComfyUI/models/clip
- download [diffusion_pytorch_model.safetensors](https://huggingface.co/stabilityai/stable-diffusion-3.5-large/blob/main/vae/diffusion_pytorch_model.safetensors) (168MB); pull it to ./ComfyUI/models/vae
- run the .bat file under the main directory (it will activate the py backend as well as the js frontend)
- drag [workflow-sd3.5-gguf.json](https://github.com/calcuis/comfy/blob/main/workflow-sd3.5-gguf.json) to the activated browser

#### Reference: [stability-ai](https://github.com/Stability-AI/sd3.5)
