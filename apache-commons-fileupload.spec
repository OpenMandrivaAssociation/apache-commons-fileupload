%global base_name       fileupload
%global short_name      commons-%{base_name}

Name:             apache-%{short_name}
Version:          1.3
Release:          3
Summary:          This package provides an api to work with html file upload
License:          ASL 2.0
Group:            Development/Java
URL:              http://commons.apache.org/%{base_name}/
Source0:          http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source1:	  MANIFEST.MF
# Depmap needed to bend javax.servlet:servlet-api to tomcat6
BuildArch:        noarch

# Portlets are not in Fedora yet
Patch0:           %{name}-remove-portlet.patch
Patch1:		  commons-fileupload-1.3-antbuild.patch

BuildRequires:    java-devel >= 0:1.6.0
BuildRequires:    junit >= 0:3.8.1
BuildRequires:    tomcat-servlet-3.0-api
BuildRequires:    apache-commons-io
BuildRequires:    ant

Requires:         java >= 0:1.6.0
Requires:         jpackage-utils
Requires:         apache-commons-io
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

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
Requires:         jpackage-utils

Obsoletes:        jakarta-%{short_name}-javadoc < 1:1.2.1-2

%description javadoc
This package contains the API documentation for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{short_name}-%{version}-src
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' NOTICE.txt

# Remove portlet stuff
#%patch0 -p0
%patch1 -p0

rm -rf src/main/java/org/apache/commons/fileupload/portlet
rm -f src/test/java/org/apache/commons/fileupload/*Portlet*

# -----------------------------------------------------------------------------

%build
export CLASSPATH=$(build-classpath commons-io tomcat-servlet-api-3.0)
ant -Dmaven.mode.offline=true -Dmaven.test.skip=true -Dcommons.manifestfile="%{SOURCE1}" -Dmaven.build.finalName=%{short_name}-%{version} package javadoc

# -----------------------------------------------------------------------------

%install
rm -rf %{buildroot}

# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
pushd %{buildroot}%{_javadir}
for jar in *-%{version}*; do
    ln -sf ${jar} `echo $jar| sed "s|apache-||g"`
    ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
    ln -sf ${jar} `echo $jar| sed "s|apache-\(.*\)-%{version}|\1|g"`
done
popd # come back from javadir

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{short_name}.pom
%add_to_maven_depmap org.apache.commons %{short_name} %{version} JPP %{short_name}

# following line is only for backwards compatibility. New packages
# should use proper groupid org.apache.commons and also artifactid
%add_to_maven_depmap %{short_name} %{short_name} %{version} JPP %{short_name}

# -----------------------------------------------------------------------------

%clean
rm -rf %{buildroot}

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

