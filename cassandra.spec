%{?scl:%scl_package cassandra}
%{!?scl:%global pkg_name %{name}}

# fedora reserved UID and GID for cassandra
%global gid_uid 143

%{!?stress:%global stress 0}

%global cqlsh_version 5.0.1

Name:		%{?scl_prefix}cassandra
Version:	3.0.12
Release:	0%{?dist}
Summary:	Client utilities for high-scale application database
# Apache (v2.0) BSD (3 clause):
# ./src/java/org/apache/cassandra/utils/vint/VIntCoding.java
License:	ASL 2.0 and BSD
URL:		http://cassandra.apache.org/
Source0:	https://github.com/apache/%{pkg_name}/archive/%{pkg_name}-%{version}.tar.gz
Source1:	%{pkg_name}.logrotate
# pom files are not generated but used are the ones from mavencentral
# because of orphaned maven-ant-task package doing the work in this case
Source2:	http://central.maven.org/maven2/org/apache/%{pkg_name}/%{pkg_name}-all/%{version}/%{pkg_name}-all-%{version}.pom
Source3:	http://central.maven.org/maven2/org/apache/%{pkg_name}/%{pkg_name}-clientutil/%{version}/%{pkg_name}-clientutil-%{version}.pom
Source4:	http://central.maven.org/maven2/org/apache/%{pkg_name}/%{pkg_name}-parent/%{version}/%{pkg_name}-parent-%{version}.pom

# remove thrift
Patch0:		%{pkg_name}-%{version}-remove-thrift.patch
# fix encoding, naming, classpaths and dependencies
Patch1:		%{pkg_name}-%{version}-build.patch
# airline0.7 imports fix in cassandra source, which is dependent on 0.6 version
# https://issues.apache.org/jira/browse/CASSANDRA-12994
Patch2:		%{pkg_name}-%{version}-airline0.7.patch
# modify installed scripts
Patch3:		%{pkg_name}-%{version}-scripts.patch
# add two more parameters for SubstituteLogger constructor in slf4j
# https://issues.apache.org/jira/browse/CASSANDRA-12996
Patch4:		%{pkg_name}-%{version}-slf4j.patch
# remove jstackjunit because of missing dependency 
# reverted upstream commit 5dd1abda21493796cbb9
Patch5:		%{pkg_name}-%{version}-jstackjunit.patch
# handle integer overflows related to size of large filesystems like Amazon EFS
# upstream issue: CASSANDRA-13067
Patch6:		%{pkg_name}-%{version}-handle-exabyte-sized-filesystems.patch

# TODO
#BuildArchitectures:	noarch

Requires:	%{pkg_name}-python2-cqlshlib = %{version}-%{release}
Requires:	%{pkg_name}-java-libs = %{version}-%{release}
Requires:	%{?scl_prefix}airline
Provides:	cqlsh = %{cqlsh_version}

%description
This package contains all client utilities for %{pkg_name}. These are:
1. Command line client used to communicate with %{pkg_name} server called cqlsh.
2. Command line interface for managing cluster called nodetool.
3. Tools for using, upgrading, and changing %{pkg_name} SSTables.

%package java-libs
Summary:	Java libraries for %{pkg_name}

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_java_common}ant
BuildRequires:	%{?scl_prefix}antlr3-tool
BuildRequires:	%{?scl_prefix}guava
BuildRequires:	%{?scl_prefix}slf4j
BuildRequires:	%{?scl_prefix_maven}apache-commons-lang3
BuildRequires:	%{?scl_prefix}jamm
BuildRequires:	%{?scl_prefix_maven}jsr-305
BuildRequires:	%{?scl_prefix}stream-lib
BuildRequires:	%{?scl_prefix}metrics
BuildRequires:	%{?scl_prefix}metrics-jvm
BuildRequires:	%{?scl_prefix}json_simple
BuildRequires:	%{?scl_prefix}compile-command-annotations
# using high-scale-lib from stephenc, no Cassandra original
#BuildRequires:	 mvn(com.boundary:high-scale-lib)
BuildRequires:	%{?scl_prefix}high-scale-lib
BuildRequires:	%{?scl_prefix}cassandra-java-driver
BuildRequires:	%{?scl_prefix}netty
BuildRequires:	%{?scl_prefix}lz4-java
BuildRequires:	%{?scl_prefix}snappy-java
BuildRequires:	%{?scl_prefix}jBCrypt
# probably won't need in the future
BuildRequires:	%{?scl_prefix}concurrentlinkedhashmap-lru
BuildRequires:	%{?scl_prefix}ohc
BuildRequires:	%{?scl_prefix}ohc-core-j8
BuildRequires:	%{?scl_prefix}snakeyaml
BuildRequires:	%{?scl_prefix}jackson
BuildRequires:	%{?scl_prefix_java_common}ecj
BuildRequires:	%{?scl_prefix}objectweb-asm
BuildRequires:	%{?scl_prefix}logback
BuildRequires:	%{?scl_prefix}apache-commons-math
BuildRequires:	%{?scl_prefix}metrics-reporter-config
BuildRequires:	%{?scl_prefix_maven}joda-time
BuildRequires:	%{?scl_prefix}compress-lzf
BuildRequires:	%{?scl_prefix}airline
BuildRequires:	%{?scl_prefix}sigar-java
# in rh-java-common: 1.9.2, needed: 1.9.4
BuildRequires:	%{?scl_prefix_java_common}ant-junit
BuildRequires:	%{?scl_prefix}byteman
BuildRequires:	%{?scl_prefix}jmh
#BuildRequires:	%{?scl_prefix}concurrent-trees
#BuildRequires:	%{?scl_prefix}HdrHistogram
#BuildRequires:	%{?scl_prefix}caffeine
# in rh-java-common: 1.7.4, needed: 1.7.7
#BuildRequires:	%{?scl_prefix_java_common}log4j-over-slf4j
# in rh-java-common: 1.7.4, needed: 1.7.7
#BuildRequires:	%{?scl_prefix_java_common}jcl-over-slf4j
# thrift deps (want to get rid of those)
#BuildRequires:	%{?scl_prefix}disruptor
#BuildRequires:	%{?scl_prefix}disruptor-thrift-server
#BuildRequires:	%{?scl_prefix}libthrift-java
# the SCL version of the package depends on rh-maven33 collection
%{?scl:Requires: %%scl_require rh-maven33}

# temporarly removed as it is optional
# using hadoop-common instead of hadoop-core, no Cassandra original
#BuildRequires:	mvn(org.apache.hadoop:hadoop-core)
#BuildRequires:	hadoop-common
#BuildRequires:	hadoop-mapreduce

%description java-libs
All the classes required by cassandra server, nodetool, sstable tools
and stress tools.

%package server
Summary:	OpenSource database server for high-scale application

%{?scl:Requires: %scl_runtime}
Requires(pre):	shadow-utils
Requires:	%{?scl_prefix}sigar
Requires:	%{pkg_name}-java-libs = %{version}-%{release}
Requires:	jctools
Requires:	procps-ng
%{?scl:Requires:	nc}
%{!?scl:Requires:	nmap-ncat}

%description server
Cassandra is a partitioned row store. Rows are organized into tables with
a required primary key. Partitioning means that Cassandra can distribute your
data across multiple machines in an application-transparent matter. Cassandra
will automatically re-partition as machines are added/removed from the cluster.
Row store means that like relational databases, Cassandra organizes data by
rows and columns. The Cassandra Query Language (CQL) is a close relative of SQL.

%package parent
Summary:	Parent POM for %{pkg_name}

%description parent
Parent POM for %{pkg_name}.

# source codes of cqlshlib are not python3 compatible, therefore using python2
%package python2-cqlshlib
Summary:	Python cqlsh library for %{pkg_name}
BuildRequires:	python2-devel
BuildRequires:	Cython
Requires:	python2-cassandra-driver
# optional timestamps in different timezones dependency
Requires:	pytz
%{?python_provide:%python_provide python2-cqlshlib}

%description python2-cqlshlib
A python library required by the commandline client used to communicate with 
%{pkg_name} server.

%if %stress
%package stress
Summary:	Stress testing utility for %{pkg_name}

%description stress
A Java-based stress testing utility for basic benchmarking and load testing a %{pkg_name} cluster.
%endif

%package javadoc
Summary:	Javadoc for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -qcn %{pkg_name}-%{version}
cp -pr %{pkg_name}-%{pkg_name}-%{version}/* .
rm -r %{pkg_name}-%{pkg_name}-%{version}

# remove binary and library files
find -name "*.class" -print -delete
find -name "*.jar" -print -delete
find -name "*.zip" -print -delete
#./lib/futures-2.1.6-py2.py3-none-any.zip
#./lib/six-1.7.3-py2.py3-none-any.zip
#./lib/cassandra-driver-internal-only-2.6.0c2.post.zip
find -name "*.so" -print -delete
find -name "*.dll" -print -delete
find -name "*.sl" -print -delete
find -name "*.dylib" -print -delete
rm -r lib/sigar-bin/sigar-x86-winnt.lib
find -name "*.exe" -print -delete
find -name "*.bat" -print -delete
find -name "*.pyc" -print -delete
find -name "*py.class" -print -delete

# copy pom files
mkdir build
cp -p %{SOURCE2} build/%{pkg_name}-%{version}.pom
cp -p %{SOURCE3} build/%{pkg_name}-clientutil-%{version}.pom
cp -p %{SOURCE4} build/%{pkg_name}-%{version}-parent.pom

# remove thrift patch
%patch0 -p1

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
# build jar repositories for dependencies
build-jar-repository lib antlr3
build-jar-repository lib antlr3-runtime
build-jar-repository lib stringtemplate4
build-jar-repository lib guava
build-jar-repository lib slf4j/api
build-jar-repository lib commons-lang3
build-jar-repository lib jamm
build-jar-repository lib jsr-305
build-jar-repository lib stream-lib
build-jar-repository lib metrics/metrics-core
build-jar-repository lib metrics/metrics-jvm
build-jar-repository lib json_simple
build-jar-repository lib compile-command-annotations
# https://bugzilla.redhat.com/show_bug.cgi?id=1308556
build-jar-repository lib high-scale-lib/high-scale-lib
build-jar-repository lib cassandra-java-driver/cassandra-driver-core
build-jar-repository lib netty/netty-all
#build-jar-repository lib netty/netty-transport-native-epoll
build-jar-repository lib lz4-java
build-jar-repository lib snappy-java
build-jar-repository lib jBCrypt
build-jar-repository lib concurrentlinkedhashmap-lru
build-jar-repository lib ohc/ohc-core
build-jar-repository lib snakeyaml
build-jar-repository lib jackson/jackson-core-asl
build-jar-repository lib jackson/jackson-mapper-asl
build-jar-repository lib ecj
build-jar-repository lib objectweb-asm/asm
build-jar-repository lib logback/logback-classic
build-jar-repository lib logback/logback-core
build-jar-repository lib commons-math3
build-jar-repository lib metrics-reporter-config/reporter-config
build-jar-repository lib metrics-reporter-config/reporter-config-base
build-jar-repository lib joda-time
build-jar-repository lib compress-lzf
build-jar-repository lib commons-cli
build-jar-repository lib airline
build-jar-repository lib jna
build-jar-repository lib sigar
# test dependencies
build-jar-repository lib junit
build-jar-repository lib ant/ant-junit
build-jar-repository lib apache-commons-io
build-jar-repository lib byteman/byteman-bmunit
build-jar-repository lib commons-collections
build-jar-repository lib jmh/jmh-core
%if 0
build-jar-repository lib concurrent-trees
# temporarly removed because it is optional
#build-jar-repository lib hadoop/hadoop-annotations
build-jar-repository lib java_cup
build-jar-repository lib commons-codec
build-jar-repository lib caffeine
# test dependencies
build-jar-repository lib ant/ant
build-jar-repository lib hamcrest/core
build-jar-repository lib HdrHistogram
# binaries dependencies
build-jar-repository lib atinject
%endif
# thrift deps (want to get rid of those)
#build-jar-repository lib libthrift
#build-jar-repository lib disruptor-thrift-server

# build patch
%patch1 -p1
# airline patch
%patch2 -p1
# scripts patch
%patch3 -p1
# slf4j patch
%patch4 -p1
# jstackjunit patch
%patch5 -p1
# filesystems patch
%patch6 -p1

# remove hadoop
rm -r src/java/org/apache/cassandra/hadoop
# remove hadoop also from pom files
%pom_remove_dep -r org.apache.hadoop: build/%{pkg_name}-%{version}.pom

# remove shaded classifier in cassandra driver from pom files
%pom_xpath_remove "pom:dependencies/pom:dependency/pom:classifier" build/%{pkg_name}-%{version}.pom

# update dependencies in the downloaded pom files to those being actually used
%pom_change_dep com.boundary: com.github.stephenc.high-scale-lib: build/%{pkg_name}-%{version}.pom

# remove thrift dependencies from the downloaded pom files
%pom_remove_dep -r com.thinkaurelius.thrift:thrift-server build/%{pkg_name}-%{version}.pom
%pom_remove_dep -r org.apache.cassandra:cassandra-thrift build/%{pkg_name}-%{version}.pom
%pom_remove_dep -r org.apache.thrift:libthrift build/%{pkg_name}-%{version}.pom
%pom_remove_dep -r org.slf4j:log4j-over-slf4j build/%{pkg_name}-%{version}.pom
%pom_remove_dep -r org.slf4j:jcl-over-slf4j build/%{pkg_name}-%{version}.pom

%mvn_package "org.apache.%{pkg_name}:%{pkg_name}-parent:pom:%{version}" parent
%mvn_package ":%{pkg_name}-clientutil" client
%if %stress
%mvn_package ":%{pkg_name}-stress" stress
%endif
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
ant jar javadoc -Drelease=true 
%{?scl:EOF}

# Build the cqlshlib Python module
pushd pylib
%{__python2} setup.py build
popd

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_artifact build/%{pkg_name}-%{version}-parent.pom
%mvn_artifact build/%{pkg_name}-%{version}.pom build/%{pkg_name}-%{version}.jar
%mvn_artifact build/%{pkg_name}-clientutil-%{version}.pom build/%{pkg_name}-clientutil-%{version}.jar
%if %stress
%mvn_artifact org.apache.%{pkg_name}:%{pkg_name}-stress:%{version} build/tools/lib/%{pkg_name}-stress.jar
%endif

%mvn_install -J build/javadoc/
%{?scl:EOF}

# Install the cqlshlib Python module
pushd pylib
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
popd

# create data and log dirs
mkdir -p %{buildroot}%{_sharedstatedir}/%{pkg_name}/data
mkdir -p %{buildroot}%{_localstatedir}/log/%{pkg_name}

# install files
install -p -D -m 644 "%{SOURCE1}"  %{buildroot}%{_sysconfdir}/logrotate.d/%{pkg_name}
install -p -D -m 755 bin/%{pkg_name} %{buildroot}%{_bindir}/%{pkg_name}
install -p -D -m 755 bin/%{pkg_name}.in.sh %{buildroot}%{_datadir}/%{pkg_name}/%{pkg_name}.in.sh
install -p -D -m 755 bin/nodetool.in.sh %{buildroot}%{_datadir}/%{pkg_name}/nodetool.in.sh
install -p -D -m 644 conf/%{pkg_name}-env.sh %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}-env.sh
install -p -D -m 644 conf/%{pkg_name}.yaml %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}.yaml
install -p -D -m 644 conf/%{pkg_name}-topology.properties %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}-topology.properties
install -p -D -m 644 conf/jvm.options %{buildroot}%{_sysconfdir}/%{pkg_name}/jvm.options
install -p -D -m 644 conf/logback-tools.xml %{buildroot}%{_sysconfdir}/%{pkg_name}/logback-tools.xml
install -p -D -m 644 conf/logback.xml %{buildroot}%{_sysconfdir}/%{pkg_name}/logback.xml
install -p -D -m 644 conf/metrics-reporter-config-sample.yaml %{buildroot}%{_sysconfdir}/%{pkg_name}/metrics-reporter-config-sample.yaml
install -p -D -m 755 bin/cqlsh.py %{buildroot}%{_bindir}/cqlsh
install -p -D -m 755 bin/nodetool %{buildroot}%{_bindir}/nodetool
install -p -D -m 755 bin/sstableloader %{buildroot}%{_bindir}/sstableloader
install -p -D -m 755 bin/sstablescrub %{buildroot}%{_bindir}/sstablescrub
install -p -D -m 755 bin/sstableupgrade %{buildroot}%{_bindir}/sstableupgrade
install -p -D -m 755 bin/sstableutil %{buildroot}%{_bindir}/sstableutil
install -p -D -m 755 bin/sstableverify %{buildroot}%{_bindir}/sstableverify
install -p -D -m 755 tools/bin/sstabledump %{buildroot}%{_bindir}/sstabledump
install -p -D -m 755 tools/bin/sstableexpiredblockers %{buildroot}%{_bindir}/sstableexpiredblockers
install -p -D -m 755 tools/bin/sstablelevelreset %{buildroot}%{_bindir}/sstablelevelreset
install -p -D -m 755 tools/bin/sstablemetadata %{buildroot}%{_bindir}/sstablemetadata
install -p -D -m 755 tools/bin/sstableofflinerelevel %{buildroot}%{_bindir}/sstableofflinerelevel
install -p -D -m 755 tools/bin/sstablerepairedset %{buildroot}%{_bindir}/sstablerepairedset
install -p -D -m 755 tools/bin/sstablesplit %{buildroot}%{_bindir}/sstablesplit
%if %stress
install -p -D -m 755 tools/bin/%{pkg_name}-stress %{buildroot}%{_bindir}/%{pkg_name}-stress
install -p -D -m 755 tools/bin/%{pkg_name}-stressd %{buildroot}%{_bindir}/%{pkg_name}-stressd
%endif

%pre server
getent group %{pkg_name} >/dev/null || groupadd -f -g %{gid_uid} -r %{pkg_name}
if ! getent passwd %{pkg_name} >/dev/null ; then
  if ! getrnt passwd %{gid_uid} >/dev/null ; then
    useradd -r -u %{gid_uid} -g %{pkg_name} -d %{_sharedstatedir}/%{pkg_name}/data \
      -s /sbin/nologin -c "Cassandra Database Server" %{pkg_name}
  else
    useradd -r -g %{pkg_name} -d %{_sharedstatedir}/%{pkg_name}/data -s /sbin/nologin \
      -c "Cassandra Database Server" %{pkg_name}
  fi
fi
exit 0

%files -f .mfiles-client
%doc README.asc CHANGES.txt NEWS.txt conf/cqlshrc.sample
%license LICENSE.txt NOTICE.txt
%attr(755, root, root) %{_bindir}/nodetool
%attr(755, root, root) %{_bindir}/sstableloader
%attr(755, root, root) %{_bindir}/sstablescrub
%attr(755, root, root) %{_bindir}/sstableupgrade
%attr(755, root, root) %{_bindir}/sstableutil
%attr(755, root, root) %{_bindir}/sstableverify
%attr(755, root, root) %{_bindir}/sstabledump
%attr(755, root, root) %{_bindir}/sstableexpiredblockers
%attr(755, root, root) %{_bindir}/sstablelevelreset
%attr(755, root, root) %{_bindir}/sstablemetadata
%attr(755, root, root) %{_bindir}/sstableofflinerelevel
%attr(755, root, root) %{_bindir}/sstablerepairedset
%attr(755, root, root) %{_bindir}/sstablesplit
%attr(755, root, root) %{_bindir}/cqlsh
%{_datadir}/%{pkg_name}/nodetool.in.sh

%files java-libs -f .mfiles
%license LICENSE.txt NOTICE.txt

%files server
%doc README.asc CHANGES.txt NEWS.txt
%license LICENSE.txt NOTICE.txt
%dir %attr(711, root, root) %{_sharedstatedir}/%{pkg_name}
%dir %attr(700, %{pkg_name}, %{pkg_name}) %{_sharedstatedir}/%{pkg_name}/data
%dir %attr(700, %{pkg_name}, %{pkg_name}) %{_localstatedir}/log/%{pkg_name}
%{_bindir}/%{pkg_name}
%{_datadir}/%{pkg_name}/%{pkg_name}.in.sh
%dir %attr(700, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/%{pkg_name}-env.sh
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/%{pkg_name}.yaml
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/%{pkg_name}-topology.properties
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/jvm.options
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/logback-tools.xml
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/logback.xml
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/metrics-reporter-config-sample.yaml
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/logrotate.d/%{pkg_name}

%files parent -f .mfiles-parent
%license LICENSE.txt NOTICE.txt

%files python2-cqlshlib
%license LICENSE.txt NOTICE.txt
%{python2_sitearch}/cqlshlib
%{python2_sitearch}/%{pkg_name}_pylib-0.0.0-py%{python2_version}.egg-info

%if %stress
%files stress -f .mfiles-stress
%license LICENSE.txt NOTICE.txt
%attr(755, root, root) %{_bindir}/%{pkg_name}-stress
%attr(755, root, root) %{_bindir}/%{pkg_name}-stressd
%{_datadir}/%{pkg_name}/%{pkg_name}.in.sh
%endif

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt

%changelog
