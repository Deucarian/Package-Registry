# Extraction Decisions

Schema version: 1

These decisions are manual-review defaults produced after hardening the analyzer. They deliberately avoid extraction from occurrence count alone.

| Candidate | Category | Repositories | Decision | Reasoning |
| --- | --- | --- | --- | --- |
| unity-object-lifetime | dedicated audit |  | runtime Common package justified | No package is created by this audit wave; this conclusion directs the next design review. |
| 03c786443e4010098790ea4115f17f047220a66f67cfb19653f4b320b7ae5047 | normalized structural clone | Object-Loading, ObjectLoading-API-Integration | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| 20d69a91512ca458a793ca07e238db173a28c4fd86028bcce1a3b13cbbffba52 | normalized structural clone | Object-Selection, ObjectSelection-CoreState-Integration | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| 57a14898cd85aa984ca53ab9fbd348ee5486c9656576c3a086b7b22d0e136cab | normalized structural clone | API, Package-Installer | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| 69fbeba1c547660e0af791d27775725cfa17f412f9b6653c603526a12b4b3716 | normalized structural clone | UI-Binding, UIBinding-CoreState-Integration | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| 6c39c301d1e205a96f5486b21d3a8f5a626878a26cc8277c88cc8dbd9a3aec2a | normalized structural clone | ObjectSelection-CoreState-Integration, Selection-Suite | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| 7934cf0376ce14461ac3e85c2932910e35fc0efc0f7884edf26a3fc69f7d6790 | normalized structural clone | Object-Selection, ObjectSelection-CoreState-Integration, Selection-Suite | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| 7d2a1120f57ad5313831cc91263ccc134fb002feea8c1c4faca58ec63b475cbc | normalized structural clone | API, Object-Loading | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| 8e445537929236429ccc43122c6b7f9d848190c77f91eb30f54c967f835ff3f9 | normalized structural clone | UI-Binding, UIBinding-CoreState-Integration | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| 99a1408e51302c37369c2a0cb17170bb60b08fefb9a0b5defceac524e1a2b79d | normalized structural clone | Object-Selection, ObjectSelection-CoreState-Integration | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| 9a5e145e2a5d32ff005b99e00717316d84a92071e77940a6acf46b4510c3190e | normalized structural clone | ObjectSelection-CoreState-Integration, Selection-Suite | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| ab5582f6483fe14214dd9cea8db2176194b89c5404646f4a0b6a9fd07cb3b08e | normalized structural clone | Selection-Suite, UIBinding-CoreState-Integration | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| b754b67455ea12d7f97ec426832c225c7027672e44eeb7fce2fc1c906c920502 | normalized structural clone | UI-Binding, UIBinding-CoreState-Integration | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| be508aa3772ff5728edfcfc341e89df97a375cfbcd0f0bbcb890afe2dee23500 | normalized structural clone | Editor, Theming | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| bed8e0d09dc0ae87372c83f7cb9f7c9c2dcd0b4ba969c8bdcd9ff94042e1dbf2 | normalized structural clone | Selection-Suite, UIBinding-CoreState-Integration | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| c2648669e159d7e86d215f3d028e1101e09fe7e2b7ac32f64c041964e1306890 | normalized structural clone | UI-Binding, UIBinding-CoreState-Integration | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| c4eeeb63e919342ebd575633925f94b27bafe595fb1b9c4cc908a61ecca07e45 | normalized structural clone | Object-Selection, UI-Binding | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| dd6391589487e332a0381d34ac33337cef7249d4f9dd4712ddefaacbb53d3f7e | normalized structural clone | Selection-Suite, UIBinding-CoreState-Integration | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| e150352bfdea54ebad982af4d6cc3144ca32686e62e76e073d007b921b8f8e67 | normalized structural clone | Core-State, Object-Selection | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| ea6aba62ff9fbfca81be2171c0d41337bf7ba696edcd0d691d47a989b5c20b41 | normalized structural clone | Object-Loading, ObjectLoading-API-Integration | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| fc204210b18f71cf0bca6015df1cf56cd9724d1224f502c5c78c9d8272cfb60c | normalized structural clone | Bootstrap, Editor | Keep local | Does not cross the production extraction threshold without manual semantic review. |
| dispose | same-symbol semantic candidate | Diagnostics, Logging, Object-Loading, Object-Selection, ObjectSelection-CoreState-Integration, Package-Installer, UI-FLow | Needs design review | Same symbol names are not enough to extract; review semantics and owner capability. |
| ondestroy | same-symbol semantic candidate | API, Core-State, Object-Loading, Object-Selection, ObjectSelection-CoreState-Integration, Selection-Suite, Session, UIBinding-CoreState-Integration | Needs design review | Same symbol names are not enough to extract; review semantics and owner capability. |
| onvalidate | same-symbol semantic candidate | API, Theming, UI-FLow | Needs design review | Same symbol names are not enough to extract; review semantics and owner capability. |
| validate | same-symbol semantic candidate | ObjectLoading-API-Integration, Package-Installer | Needs design review | Same symbol names are not enough to extract; review semantics and owner capability. |
| validatekey | same-symbol semantic candidate | Core-State, Object-Selection | Needs design review | Same symbol names are not enough to extract; review semantics and owner capability. |
