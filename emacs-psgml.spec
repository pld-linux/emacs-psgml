Summary:	A GNU Emacs major mode for editing SGML documents
Name:		emacs-psgml
Version:	1.2.5
Release:	1
License:	GPL
Group:		Applications/Editors/Emacs
Source0:	ftp://ftp.lysator.liu.se/pub/sgml/psgml-%{version}.tar.gz
# Source0-md5:	d4f346b0242035e54860b29d7466b0a2
Patch0:		%{name}-install-info.patch
Patch1:		%{name}-DESTDIR.patch
Requires:	emacs
Requires:	sgml-common
BuildRequires:	emacs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define psgmldir %{_datadir}/emacs/site-lisp/psgml/

%description
Emacs is an advanced and extensible editor. An Emacs major mode
customizes Emacs for editing particular types of text documents. PSGML
is a major mode for SGML (a markup language) documents. PSGML provides
several functionalities for editing SGML documents: indentation
according to element nesting depth and identification of structural
errors (but it is not a validating SGML parser); menus and commands
for inserting tags with only the contextually valid tags; attribute
values can be edited in a separate window with information about types
and defaults; structure based editing includes movement and killing;
and also several commands for folding editing.

%prep
%setup -q -n psgml-%{version}
%patch0 -p1
%patch1 -p1

%build
%configure2_13

%{__make} \
	lispdir=%{_datadir}/emacs/site-lisp/psgml

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_datadir}/emacs/site-lisp/site-start.d}

%{__make} install install-info \
	lispdir=%{_datadir}/emacs/site-lisp/psgml \
	DESTDIR=$RPM_BUILD_ROOT

cat > $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/psgml-init.el << __ELISP__
(setq load-path (append load-path '("%{_datadir}/emacs/site-lisp/psgml")))

(autoload 'sgml-mode "psgml" "Major mode for editing SGML." t)
(autoload 'xml-mode "psgml" "Major mode for editing XML." t)
(if (not (getenv "SGML_CATALOG_FILES"))
(defvar sgml-catalog-files '("CATALOG" "catalog" "%{_sysconfdir}/sgml/catalog" "%{_prefix}/lib/sgml/CATALOG" "%{_prefix}/lib/sgml-tools/dtd/catalog"))
  "*List of catalog entry files.
The files are in the format defined in the SGML Open Draft Technical
Resolution on Entity Management.")
(put 'sgml-catalog-files 'sgml-type 'list)
__ELISP__


%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc psgml.ps README.psgml
%dir %{psgmldir}
%{psgmldir}/*
%{_datadir}/emacs/site-lisp/site-start.d/*
%{_infodir}/psgml*
