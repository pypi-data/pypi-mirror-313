CHANGES
*******

4.1 (2024-12-04)
================

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7.

- The tests are not compatible with (yanked) ``Chameleon`` 4.3.0, thus not
  allowing to use this version.

- Update translation handling to be compatible with Chameleon 4.3+: do not
  break on unhashable message ids, just return them.


4.0 (2023-02-09)
================

- Drop support for Python 2.7, 3.4, 3.5, 3.6.

- Add support for Python 3.7, 3.8, 3.9, 3.10, 3.11.


3.0.1 (2018-01-12)
==================

- Rearrange tests such that Travis CI can pick up all functional tests too.

3.0.0 (2018-01-11)
==================

- Python 3 compatibility.

1.0.4 (2014-07-29)
==================

- Improve the performances of the translate mechanism with Chameleon
  2.10 or more recent.

1.0.3 (2012-10-12)
==================

- Fix broken translations when using Chameleon 2.9 or more recent.

1.0.2 (2012-05-07)
==================

- With not using the z3c.pt PageTemplateFile baseclass, the behaviour of
  finding the template file relative to the module was lost. This has been
  fixed.

1.0.1 (2012-05-03)
==================

- Make sure the minimal version requirements are defined.

1.0 (2012-05-01)
================

- The ``target_language`` mangling was lost in version 1.0rc4.
  Copied from z3c.pt.

1.0rc4 (2012-01-03)
===================

- Update to newes Chameleon 2.7.1
- Using some Components/Expressions directly from Chameleon instead of z3c.pt

1.0rc3 (2011-07-14)
===================

- Rename megrok.chameleon into grokcore.chameleon to make it an official part
  of Grok.

Earlier versions
================

- Earlier versions of grokcore.chameleon came by the name megrok.chameleon.
