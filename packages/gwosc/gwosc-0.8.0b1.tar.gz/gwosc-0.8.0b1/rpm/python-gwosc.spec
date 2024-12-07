%define srcname gwosc
%define version 0.7.1
%define release 1

Name:      python-%{srcname}
Version:   %{version}
Release:   %{release}%{?dist}
Summary:   A python interface to the Gravitational-Wave Open Science Center data archive

License:   MIT
Url:       https://gwosc.readthedocs.io
Source0:   %pypi_source

Packager:  Duncan Macleod <duncan.macleod@ligo.org>
Vendor:    Duncan Macleod <duncan.macleod@ligo.org>

BuildArch: noarch
Prefix:    %{_prefix}

# -- build requirements

BuildRequires: python3-devel >= 3.5.0
BuildRequires: python3dist(pip)
BuildRequires: python3dist(setuptools) >= 30.3.0
BuildRequires: python3dist(wheel)

# tests
BuildRequires: python3dist(requests) >= 1.0.0
BuildRequires: python3dist(pytest)
BuildRequires: python3dist(requests-mock) >= 1.5.0

# -- packages

# src.rpm
%description
The `gwosc` package provides an interface to querying the open data
releases hosted on <https://gwosc.org> from the GEO, LIGO,
and Virgo gravitational-wave observatories.

# python3X-gwosc

%package -n python3-%{srcname}
Summary:  %{summary}
Requires: python3dist(requests) >= 1.0.0
%description -n python3-%{srcname}
The `gwosc` package provides an interface to querying the open data
releases hosted on <https://gwosc.org> from the GEO, LIGO,
and Virgo gravitational-wave observatories.
%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

# -- build steps

%prep
%autosetup -n %{srcname}-%{version}

# for RHEL < 9 hack together setup.{cfg,py} for old setuptools
%if 0%{?rhel} && 0%{?rhel} < 10
cat > setup.cfg << SETUP_CFG
[metadata]
name = %{srcname}
version = %{version}
author-email = %{packager}
description = %{summary}
license = %{license}
license_files = LICENSE
url = %{url}
[options]
packages = find:
python_requires = >=3.6
install_requires =
  requests >= 1.0.0
SETUP_CFG
%endif
%if %{undefined pyproject_wheel}
cat > setup.py << SETUP_PY
from setuptools import setup
setup()
SETUP_PY
%endif

%build
%if %{defined pyproject_wheel}
%pyproject_wheel
%else
%py3_build_wheel
%endif

%install
%if %{defined pyproject_install}
%pyproject_install
%else
%py3_install_wheel *.whl
%endif

%check
export PYTHONPATH="%{buildroot}%{python3_sitelib}"
%pytest --pyargs %{srcname} -m "not remote"

# -- changelog

%changelog
* Thu Apr 20 2023 Duncan Macleod <duncan.macleod@ligo.org> - 0.7.1-1
- update to 0.7.1

* Mon Apr 10 2023 Duncan Macleod <duncan.macleod@ligo.org> - 0.7.0-1
- update to 0.7.0

* Thu Aug 12 2021 Duncan Macleod <duncan.macleod@ligo.org> - 0.6.1-1
- update to 0.6.1

* Mon Aug 09 2021 Duncan Macleod <duncan.macleod@ligo.org> - 0.6.0-1
- update to 0.6.0

* Wed May 19 2021 Duncan Macleod <duncan.macleod@ligo.org> - 0.5.8-1
- update to 0.5.8

* Wed May 12 2021 Duncan Macleod <duncan.macleod@ligo.org> - 0.5.7-1
- update to 0.5.7
- add setuptools-scm and wheel build requirements
- run tests in color

* Thu Aug 27 2020 Duncan Macleod <duncan.macleod@ligo.org> - 0.5.6-1
- update to 0.5.6
- add python3-requests-mock as a test requirement

* Mon Jul 27 2020 Duncan Macleod <duncan.macleod@ligo.org> - 0.5.5-1
- update to 0.5.5

* Sun Jul 26 2020 Duncan Macleod <duncan.macleod@ligo.org> - 0.5.4-1
- update to 0.5.4

* Wed Apr 22 2020 Duncan Macleod <duncan.macleod@ligo.org> - 0.5.3-1
- update to 0.5.3

* Wed Mar 18 2020 Duncan Macleod <duncan.macleod@ligo.org> - 0.5.2-1
- update to 0.5.2

* Tue Mar 17 2020 Duncan Macleod <duncan.macleod@ligo.org> - 0.5.1-1
- update to 0.5.1

* Tue Mar 17 2020 Duncan Macleod <duncan.macleod@ligo.org> - 0.5.0-1
- drop support for python2

* Tue Mar 12 2019 Duncan Macleod <duncan.macleod@ligo.org> - 0.4.3-1
- bug fix release, see github releases for details

* Mon Mar 11 2019 Duncan Macleod <duncan.macleod@ligo.org> - 0.4.2-1
- bug fix release, see github releases for details

* Thu Feb 28 2019 Duncan Macleod <duncan.macleod@ligo.org> - 0.4.1-1
- development release to include catalogue parsing

* Mon Oct 1 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 0.3.4 testing bug-fix release

* Mon Jul 9 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 0.3.3 packaging bug-fix release
