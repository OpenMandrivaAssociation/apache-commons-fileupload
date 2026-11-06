Name:		apache-commons-fileupload
Version:	1.6.0
Release:	1
Summary:	Multipart form-data parser for servlets
Group:		Development/Java
License:	ASL 2.0
URL:		https://commons.apache.org/proper/commons-fileupload/
Source0:	https://github.com/apache/commons-fileupload/archive/refs/tags/rel/commons-fileupload-%{version}.tar.gz#/commons-fileupload-%{version}.tar.gz

BuildArch:	noarch
Obsoletes:	%{name}-javadoc < %{version}
# The site checkout profile is active when site-content is absent, and
# antrun is on the sysjar keep list.
%global sysjar_drops --drop org.apache.maven.plugins:maven-antrun-plugin
BuildRequires:	mvn(org.apache.commons:commons-parent:pom::)
BuildRequires:	mvn(org.apache:apache:pom::)
BuildRequires:	mvn(commons-io:commons-io)
BuildRequires:	mvn(javax.servlet:javax.servlet-api)
BuildRequires:	mvn(net.java:jvnet-parent:pom::)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name commons-fileupload --link %{name} --alias org.apache.commons:commons-fileupload

%description
Apache Commons FileUpload parses multipart/form-data in a servlet
request. 1.6.0 needs Java 8, limits each part header, and accepts
multipart/related. The portlet classes are left out: portlet-api is
not packaged. Tests are skipped.

%prep
%autosetup -n commons-fileupload-rel-commons-fileupload-%{version}
# The published servlet coordinate is javax.servlet:javax.servlet-api.
# portlet-api is not packaged, and Maven still resolves a provided dep.
python - <<'PY'
import re
import shutil
from pathlib import Path

pom = Path("pom.xml")
text = pom.read_text()
old = "<artifactId>servlet-api</artifactId>\n      <version>2.5</version>"
new = "<artifactId>javax.servlet-api</artifactId>\n      <version>4.0.1</version>"
if old not in text:
    raise SystemExit("servlet-api dependency not found")
text = text.replace(old, new, 1)
text, n = re.subn(
    r"\s*<dependency>\s*<groupId>portlet-api</groupId>\s*<artifactId>portlet-api</artifactId>.*?</dependency>",
    "",
    text,
    count=1,
    flags=re.S,
)
if n != 1:
    raise SystemExit(f"portlet dep {n}")
pom.write_text(text)
shutil.rmtree("src/main/java/org/apache/commons/fileupload/portlet")
PY

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt README.md
