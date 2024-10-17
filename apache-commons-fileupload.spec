%{?_javapackages_macros:%_javapackages_macros}
# Need this build path
%define fedora 20
%global base_name       fileupload
%global short_name      commons-%{base_name}

Name:             apache-%{short_name}
Version:          1.3.1
Release:          5.3
Summary:          This package provides an api to work with html file upload
License:          ASL 2.0
Group:            Development/Java
URL:              https://commons.apache.org/%{base_name}/
Source0:          http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
BuildArch:        noarch

BuildRequires:    java-devel >= 1:1.6.0
BuildRequires:    maven-local
BuildRequires:    junit >= 0:3.8.1
BuildRequires:    servlet
BuildRequires:    apache-commons-io
BuildRequires:    maven-antrun-plugin
BuildRequires:    maven-assembly-plugin
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-doxia-sitetools
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-plugin-bundle
BuildRequires:    maven-release-plugin
BuildRequires:    maven-resources-plugin
%if 0%{?fedora}
BuildRequires:    portlet-2.0-api
%endif

Requires:         java-headless >= 1:1.6.0
Requires:         jpackage-utils
Requires:         apache-commons-io
%if 0%{?fedora}
Requires:         portlet-2.0-api
%endif

%description
The javax.servlet package lacks support for rfc 1867, html file
upload.  This package provides a simple to use api for working with
such data.  The scope of this package is to create a package of Java
utility classes to read multipart/form-data within a
javax.servlet.http.HttpServletRequest

%package javadoc
Summary:          API documentation for %{name}
Group:            Documentation
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{short_name}-%{version}-src
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' NOTICE.txt

%if 0%{?fedora}
# fix gId
sed -i "s|<groupId>portlet-api</groupId>|<groupId>javax.portlet</groupId>|" pom.xml
%else
# Non-Fedora: remove portlet stuff
%pom_remove_dep portlet-api:portlet-api
%pom_xpath_remove pom:properties/pom:commons.osgi.import
%pom_xpath_remove pom:properties/pom:commons.osgi.dynamicImport
rm -r src/main/java/org/apache/commons/fileupload/portlet
rm src/test/java/org/apache/commons/fileupload/*Portlet*
%endif

# -----------------------------------------------------------------------------

%build
# fix build with generics support
# tests fail to compile because they use an obsolete version of servlet API (2.4)
mvn-rpmbuild -Dmaven.test.skip=true -Dmaven.compile.source=1.5 -Dmaven.compile.target=1.5 install javadoc:javadoc
# -----------------------------------------------------------------------------

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 target/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
pushd $RPM_BUILD_ROOT%{_javadir}
    ln -sf %{name}.jar %{short_name}.jar
popd # come back from javadir

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{short_name}.pom
%add_maven_depmap JPP-%{short_name}.pom %{short_name}.jar -a "org.apache.commons:%{short_name}"

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{short_name}.jar

%files javadoc
%doc LICENSE.txt NOTICE.txt
%doc %{_javadocdir}/%{name}

# -----------------------------------------------------------------------------

%changelog
* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-5
- Remove legacy Obsoletes/Provides for jakarta-commons

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-3
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.3.1-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Feb 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-1
- Update to upstream version 1.3.1
- Remove unused patched

* Thu Feb  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-5
- Add backported upstream patch to fix DoS vulnerability
- Resolves: CVE-2014-0050

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-3
- Remove unneeded BR: maven-idea-plugin

* Thu Apr 18 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.3-2
- Use pom macros over patch.
- Remove surefire maven plugin since tests are skipped anyway.

* Thu Mar 28 2013 Michal Srb <msrb@redhat.com> - 1.3-1
- Update to upstream version 1.3

* Mon Mar 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.2-11
- Disable tests (they use obsolete servlet API 2.4)
- Resolves: rhbz#913878

* Thu Feb 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.2-10
- Add missing BR: maven-local

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.2.2-8
- Conditionally build portlet-2.0-api support in Fedora only

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.2-6
- Fix up patches to apply, cleanup spec old coments
- Fix surefire plugin dependency to use new name

* Tue May 29 2012 gil cattaneo <puntogil@libero.it> 1.2.2-5
- Add portlet-2.0-api support (required by springframework).

* Fri Mar  2 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> 1.2.2-4
- Fix build and update to latest guidelines

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Chris Spike <chris.spike@arcor.de> 1.2.2-1
- Updated to 1.2.2
- Fixed License tag
- tomcat5 -> tomcat6 BRs/Rs
- Fixed wrong EOL encodings

* Thu Jul  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.1-4
- Add license to javadoc subpackage

* Thu May 20 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.1-3
- Added Requires on jpackage-utils for javadoc

* Thu May 20 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.1-2
- Rename package (jakarta-commons-fileupload->apache-commons-fileupload)
- Re-did whole spec file

* Wed Jan  6 2010 Mary Ellen Foster <mefoster at gmail.com> - 1:1.2.1-1
- Update to newest version; include Maven metadata

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-9.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-8.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.0-7.3
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.0-7jpp.2
- Autorebuild for GCC 4.3

* Tue Apr 17 2007 Permaine Cheung <pcheung@redhat.com> - 1:1.0-6jpp.2
- Update spec file as per fedora review

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> - 1:1.0-6jpp.1
- Added missing requirements.

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 1.0-5jpp_3fc
- Requires(post/postun): coreutils

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 1:1.0-5jpp_2fc
- Rebuilt

* Thu Jul 20 2006 Deepak Bhole <dbhole@redhat.com> - 1:1.0-5jpp_1fc
- Added conditional native compilation.

* Wed Apr 26 2006 Fernando Nasser <fnasser@redhat.com> - 1:1.0-4jpp
- First JPP 1.7 build

* Fri Oct 22 2004 Fernando Nasser <fnasser@redhat.com> - 1:1.0-3jpp
- Patch to build with servletapi5
- Add missing dependency on ant-junit

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 1:1.0-2jpp
- Rebuild with ant-1.6.2

* Sat Jun 28 2003 Ville Skyttä <ville.skytta at iki.fi> - 1:1.0-1jpp
- Update to 1.0.
- Add Epochs to dependencies.
- Nuke beanutils dependency.
- Versionless javadoc dir symlinks.

* Tue Mar 25 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> - 1:1.0-0.beta1.4jpp
- for jpackage-utils 1.5

* Mon Mar 10 2003 Henri Gomez <hgomez@users.sourceforge.net> - 1:1.0-0.beta1.3jpp
- rebuild with correct ant (avoid corrupted archive)

* Fri Mar 07 2003 Henri Gomez <hgomez@users.sourceforge.net> - 1:1.0-0.beta1.2jpp
- replace servlet23 requirement by servlet4api

* Wed Feb 26 2003 Ville Skyttä <ville.skytta at iki.fi> - 1:1.0-0.beta1.1jpp
- Update to 1.0 beta 1 (no code changes from cvs20030115).
- Fix requirements.

* Wed Jan 15 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.0-1jpp
- 1.0 (cvs 20030115)
- first jPackage release

