"""Dapi Writer"""

from opendapi.utils import has_underlying_model_changed
from opendapi.validators.defs import CollectedFile
from opendapi.writers.base import BaseFileWriter


class DapiFileWriter(BaseFileWriter):
    """Writer for Dapi files"""

    def skip(
        self, collected_file: CollectedFile
    ) -> bool:  # pylint: disable=unused-argument
        """
        Skip autoupdate if there is no material change to the model

        This is necessary for organic onboarding, since otherwise features being on will
        always lead to Dapis being autoupdated, since more will be returned from
        base_template_for_autoupdate, and the content will have changed, regardless of if
        the model was updated organically

        NOTE: To work properly, needs base_collected_files - otherwise the fallback is to always
              autoupdate, which is safest, but noisiest
        """

        # the model was deleted, a write would just be the same as the original
        if not collected_file.generated:
            return True

        if base_collected_file := self.base_collected_files.get(
            collected_file.filepath
        ):

            # if we ever had a file written then it was onboarded
            was_onboarded = base_collected_file.original or collected_file.original

            return not (
                # the generated output allows us to compare the ORM state
                has_underlying_model_changed(
                    collected_file.generated, base_collected_file.generated
                )
                # If the ORM state is the same, someone could have still edited the file manually,
                # and we need to make sure that they did it in a valid way. We therefore compare
                # the file state now versus the ORM state now, but we note that we must allow
                # for nullability changes (i.e. from the portal), as those are valid. Merged
                # uses the nullability changes from the portal, but also reflects the current
                # ORM state, and so we compare against that
                or (
                    was_onboarded
                    and has_underlying_model_changed(
                        collected_file.merged, collected_file.original
                    )
                )
            )

        # neither the model nor the file existed at base,
        # so we do not skip
        return False
