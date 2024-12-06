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

        if base_collected_file := self.base_collected_files.get(
            collected_file.filepath
        ):
            return not (
                # the generated output at a given step tells you the state of the model
                # directly from the ORM, and so those are what we compare.
                has_underlying_model_changed(
                    collected_file.generated, base_collected_file.generated
                )
                # If the Dapi was not onboarded, we are okay if generated and original differ.
                # But, if the Dapi was onboarded, we must keep the Dapi in sync with the model,
                # i.e. if someone removes fields on their own from the Dapi
                or (
                    collected_file.original
                    and has_underlying_model_changed(
                        collected_file.generated, collected_file.original
                    )
                )
            )
        return False
