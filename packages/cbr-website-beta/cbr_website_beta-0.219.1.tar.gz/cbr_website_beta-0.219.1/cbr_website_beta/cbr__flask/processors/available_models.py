from cbr_website_beta.apps.llms.LLMs__Platforms import LLMs__Platforms

llms_platforms = LLMs__Platforms()

def available_models():
   return llms_platforms.model_options()