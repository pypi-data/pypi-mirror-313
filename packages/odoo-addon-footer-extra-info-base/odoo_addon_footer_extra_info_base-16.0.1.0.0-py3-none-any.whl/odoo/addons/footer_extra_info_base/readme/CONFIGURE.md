In order to include additional information in the PDF footer of a given model, it is necessary to create a new module that depends on this one and do the following:

1.	Inherit the abstract class "footer.extra.info.mixin" from the model which could add information to the PDF footer.
2.	Override the _compute_footer_extra_info method in "footer.extra.info.mixin" to set a value in field footer_extra_info, which is the field that contains the information that is added to the PDF footer.
