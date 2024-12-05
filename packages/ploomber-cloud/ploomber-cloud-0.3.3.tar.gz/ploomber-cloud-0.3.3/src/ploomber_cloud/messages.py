#######################################################
# Define messages for specific prompts and cases here #
#######################################################

from ploomber_cloud.models import AuthCompatibleFeatures


FEATURE_PROMPT_MSG = "Please specify the feature for which to add authentication"
CARRIED_OVER_CREDENTIALS_MSG = "Your credentials were carried over from the old \
configuration.\n If you wish to modify them, please use ploomber-cloud auth\
--add --overwrite"


def no_authentication_error_msg(feature: AuthCompatibleFeatures):
    return f"No authentication found for {feature.value}."
