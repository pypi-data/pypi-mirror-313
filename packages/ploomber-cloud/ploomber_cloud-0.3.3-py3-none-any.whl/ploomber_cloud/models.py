from enum import Enum


##################
# AUTHENTICATION #
##################


# TODO: sync this code with the backend code, exact same enum is found there.
# HACK: we have 2 separate enums keep it simple. Eventually a single source
# of truth would be better.
class AuthCompatibleFeatures(Enum):
    """
    List the available features for which we can enable nginx authentication
    """

    ANALYTICS = "analytics"
    MAIN_APP = "main_app"

    @staticmethod
    def get_required_permissions_for_feature(
        feature: "AuthCompatibleFeatures",
    ) -> list[str]:
        """
        Get the list of required permissions for a given feature.

        This static method retrieves the list of permissions associated with a specific
        AuthCompatibleFeatures enum value. It uses the permission_map to look up the
        corresponding permissions for the given feature.

        Params:
            feature (AuthCompatibleFeatures): The feature for which to retrieve
            permissions.

        Returns:
            list[str]: A list of permission strings required for the specified feature.
                    Returns an empty list if the feature is not found in the
                    permission_map.

        Example:
            permissions = AuthCompatibleFeatures.get_required_permissions_for_feature(
                AuthCompatibleFeatures.ANALYTICS
            )
            # Returns: ["viewAnalyticsReport"]
        """
        return _permission_map.get(feature, [])


# Mapping of features to their corresponding permissions
# The permissions can be found in the configurations folder
# under in the user tier json in the allowedFeatures section.
_permission_map: dict["AuthCompatibleFeatures", list[str]] = {
    AuthCompatibleFeatures.ANALYTICS: ["viewAnalyticsReport"],
}


#############
# USER TIER #
#############


# ensure that the value of each enum member matches the name of the .json file config
class UserTiers(Enum):
    """
    Enum for user tiers
    """

    COMMUNITY = "community"
    PRO = "pro"
    TEAMS = "teams"
