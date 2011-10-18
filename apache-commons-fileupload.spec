%global base_name       fileupload
%global short_name      commons-%{base_name}

Name:             apache-%{short_name}
Version:          1.2.2
Release:          3
Summary:          This package provides an api to work with html file upload
License:          ASL 2.0
Group:            Development/Java
URL:              http://commons.apache.org/%{base_name}/
Source0:          http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
# Depmap needed to bend javax.servlet:servlet-api to tomcat6
Source1:          %{short_name}.depmap
BuildArch:        noarch

# Portlets are not in Fedora yet
Patch0:           %{name}-remove-portlet.patch

BuildRequires:    java-devel >= 0:1.6.0
BuildRequires:    junit >= 0:3.8.1
BuildRequires:    servlet25
BuildRequires:    apache-commons-io
BuildRequires:    maven-antrun-plugin
BuildRequires:    maven-assembly-plugin
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-doxia-sitetools
BuildRequires:    maven-idea-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-plugin-bundle
BuildRequires:    maven-release-plugin
BuildRequires:    maven-resources-plugin
#Should be replaced by maven-surefire-plugin after f15 branch
BuildRequires:    maven-surefire-maven-plugin


Requires:         java >= 0:1.6.0
Requires:         jpackage-utils >= 0:1.7.5
Requires:         apache-commons-io
Requires(post):   jpackage-utils >= 0:1.7.5
Requires(postun): jpackage-utils >= 0:1.7.5

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:         jakarta-%{short_name} = 1:%{version}-%{release}
Obsoletes:        jakarta-%{short_name} < 1:1.2.1-2

%description
The javax.servlet package lacks support for rfc 1867, html file
upload.  This package provides a simple to use api for working with
such data.  The scope of this package is to create a package of Java
utility classes to read multipart/form-data within a
javax.servlet.http.HttpServletRequest

%package javadoc
Summary:          API documentation for %{name}
Group:            Development/Java
Requires:         jpackage-utils >= 0:1.7.5

Obsoletes:        jakarta-%{short_name}-javadoc < 1:1.2.1-2

%description javadoc
This package contains the API documentation for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{short_name}-%{version}-src
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' NOTICE.txt

# Remove portlet stuff
%patch0 -p0
rm -rf src/java/org/apache/commons/fileupload/portlet
rm -f src/test/org/apache/commons/fileupload/*Portlet*

# -----------------------------------------------------------------------------

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven2.jpp.depmap.file="%{SOURCE1}" \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

# -----------------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 target/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}*; do
    ln -sf ${jar} `echo $jar| sed "s|apache-||g"`
    ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
    ln -sf ${jar} `echo $jar| sed "s|apache-\(.*\)-%{version}|\1|g"`
done
popd # come back from javadir

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{short_name}.pom
%add_to_maven_depmap org.apache.commons %{short_name} %{version} JPP %{short_name}

# following line is only for backwards compatibility. New packages
# should use proper groupid org.apache.commons and also artifactid
%add_to_maven_depmap %{short_name} %{short_name} %{version} JPP %{short_name}

# -----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# -----------------------------------------------------------------------------

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*.pom

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

# -----------------------------------------------------------------------------

