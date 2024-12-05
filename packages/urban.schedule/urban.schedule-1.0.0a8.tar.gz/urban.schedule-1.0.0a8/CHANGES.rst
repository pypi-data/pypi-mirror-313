Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

1.0.0a8 (2024-12-03)
--------------------

New features:


- Add two new creation conditions `IsPloneMeetingCollegeDone` and `IsPloneMeetingCouncilDone`.
  [aduchene]
  Add two new start dates `PloneMeetingCollegeDecidedDate` and `PloneMeetingCouncilDecidedDate`.
  [aduchene]
  Add roaddecree tasks for liege.
  [aduchene] (URB-3150)
- Add roaddecree tasks for classic.
  [aduchene] (URB-3151)


1.0.0a7 (2024-10-25)
--------------------

Bug fixes:


- Update schedule config for reception (skip existing)
  [daggelpop] (URB-3005)


1.0.0a6 (2024-10-16)
--------------------

New features:


- Add two new creation conditions `IsPloneMeetingCollegeDone` and `IsPloneMeetingCouncilDone`.
  [aduchene]
  Add two new start dates `PloneMeetingCollegeDecidedDate` and `PloneMeetingCouncilDecidedDate`.
  [aduchene]
  Add roaddecree tasks for liege.
  [aduchene] (URB-3150)


1.0.0a5 (2024-10-01)
--------------------

Bug fixes:


- Add amended plans translations
  [daggelpop] (URB-3005)


1.0.0a4 (2024-06-27)
--------------------

New features:


- Add start_date and conditional adapter for amended plans
  [daggelpop]
  Add task config for amended plans
  [daggelpop]
  Add config for `recepisse-de-plans-modificatifs` event
  [daggelpop]
  Adapt `AcknowledgmentLimitDate` for `IntentionToSubmitAmendedPlans`
  [daggelpop]
  Change opinion FD delay for codt 2024 change
  [jchandelle] (URB-3005)


1.0.0a3 (2024-03-30)
--------------------

New features:


- Store checking completion task config for liege.
  Store reception task config for CODT Buildlicence and CU on Urban classic.
  [daggelpop, mpeeters] (URB-3005)


Internal:


- Add french translations for conditions.
  Handle specific configuration for Liege and Urban classic.
  Improve import of config by adding `match_filename` optional parameter to only import one config filename.
  [mpeeters] (URB-3005)


1.0.0a2 (2024-03-14)
--------------------

Bug fixes:


- Fix import uid and @id and fix existing content handling
  Fix enum dependency
  [jchandelle] (URB-3005)


1.0.0a1 (2024-03-12)
--------------------

New features:


- Add conditions to determine if the current content is under the new reform or not
  [mpeeters] (URB-3004)
- Add upgrade step to import schedule config
  Adapt `urban.schedule.start_date.acknowledgment_limit_date` to handle the new rules of the CODT reform
  [jchandelle, mpeeters] (URB-3005)
