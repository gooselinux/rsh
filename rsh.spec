Summary: Clients for remote access commands (rsh, rlogin, rcp)
Name: rsh
Version: 0.17
Release: 60%{?dist}
License: BSD
Group: Applications/Internet

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl, ncurses-devel, pam-devel, audit-libs-devel

URL: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit
Source0 ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-rsh-%{version}.tar.gz
Source1: rexec.pam
Source2: rlogin.pam
Source3: rsh.pam
# Source is no longer publicly available.
Source4: rexec-1.5.tar.gz
Source5: rsh-xinetd
Source6: rlogin-xinetd
Source7: rexec-xinetd

Patch1: netkit-rsh-0.17-sectty.patch
# Make rexec installation process working
Patch2: netkit-rsh-0.17-rexec.patch
Patch3: netkit-rsh-0.10-stdarg.patch
# Improve installation process
Patch4: netkit-rsh-0.16-jbj.patch
# Link rshd against libpam
Patch8: netkit-rsh-0.16-jbj4.patch
Patch9: netkit-rsh-0.16-prompt.patch
Patch10: netkit-rsh-0.16-rlogin=rsh.patch
# Improve documentation
Patch11: netkit-rsh-0.16-nokrb.patch
# Remove spurious double-reporting of errors
Patch12: netkit-rsh-0.17-pre20000412-jbj5.patch
# RH #42880
Patch13: netkit-rsh-0.17-userandhost.patch
# Don't strip binaries during installation
Patch14: netkit-rsh-0.17-strip.patch
# RH #67362
Patch15: netkit-rsh-0.17-lfs.patch
# RH #57392
Patch16: netkit-rsh-0.17-chdir.patch
# RH #63806
Patch17: netkit-rsh-0.17-pam-nologin.patch
# RH #135643
Patch19: netkit-rsh-0.17-rexec-netrc.patch
# RH #68590
Patch20: netkit-rsh-0.17-pam-sess.patch
# RH #67361
Patch21: netkit-rsh-0.17-errno.patch
# RH #118630
Patch22: netkit-rsh-0.17-rexec-sig.patch
# RH #135827
Patch23: netkit-rsh-0.17-nohost.patch
# RH #122315
Patch24: netkit-rsh-0.17-ignchld.patch
# RH #146464
Patch25: netkit-rsh-0.17-checkdir.patch
Patch26: netkit-rsh-0.17-pam-conv.patch
# RH #174045
Patch27: netkit-rsh-0.17-rcp-largefile.patch
# RH #174146
Patch28: netkit-rsh-0.17-pam-rhost.patch
# RH #178916
Patch29: netkit-rsh-0.17-rlogin-linefeed.patch
Patch30: netkit-rsh-0.17-ipv6.patch
Patch31: netkit-rsh-0.17-pam_env.patch
Patch33: netkit-rsh-0.17-dns.patch
Patch34: netkit-rsh-0.17-nohostcheck-compat.patch
# RH #448904
Patch35: netkit-rsh-0.17-audit.patch
Patch36: netkit-rsh-0.17-longname.patch
# RH #440867
Patch37: netkit-rsh-0.17-arg_max.patch
Patch38: netkit-rsh-0.17-rh448904.patch
Patch39: netkit-rsh-0.17-rh461903.patch

%description
The rsh package contains a set of programs which allow users to run
commands on remote machines, login to other machines and copy files
between machines (rsh, rlogin and rcp).  All three of these commands
use rhosts style authentication.  This package contains the clients
needed for all of these services.
The rsh package should be installed to enable remote access to other
machines

%package server
Summary: Servers for remote access commands (rsh, rlogin, rcp)
Group: System Environment/Daemons
Requires: pam, /etc/pam.d/system-auth, xinetd

%description server
The rsh-server package contains a set of programs which allow users
to run commands on remote machines, login to other machines and copy
files between machines (rsh, rlogin and rcp).  All three of these
commands use rhosts style authentication.  This package contains the
servers needed for all of these services.  It also contains a server
for rexec, an alternate method of executing remote commands.
All of these servers are run by xinetd and configured using
/etc/xinet.d/ and PAM.

The rsh-server package should be installed to enable remote access
from other machines

%prep
%setup -q -n netkit-rsh-%{version} -a 4
%patch1 -p1 -b .sectty
%patch2 -p1 -b .rexec
%patch3 -p1 -b .stdarg
%patch4 -p1 -b .jbj
%patch8 -p1 -b .jbj4
%patch9 -p1 -b .prompt
%patch10 -p1 -b .rsh
%patch11 -p1 -b .rsh.nokrb
%patch12 -p1 -b .jbj5
%patch13 -p1 -b .userandhost
%patch14 -p1 -b .strip
%patch15 -p1 -b .lfs
%patch16 -p1 -b .chdir
%patch17 -p1 -b .pam-nologin
%patch19 -p1 -b .rexec-netrc
%patch20 -p1 -b .pam-sess
%patch21 -p1 -b .errno
%patch22 -p1 -b .rexec-sig
%patch23 -p1 -b .nohost
%patch24 -p1 -b .ignchld
%patch25 -p1 -b .checkdir
%patch26 -p1 -b .pam-conv
%patch27 -p1 -b .largefile
%patch28 -p1 -b .pam-rhost
%patch29 -p1 -b .linefeed
%patch30 -p1 -b .ipv6
%patch31 -p1 -b .pam_env
%patch33 -p1 -b .dns
%patch34 -p1 -b .compat
%patch35 -p1 -b .audit
%patch36 -p1 -b .longname
%patch37 -p1 -b .arg_max
%patch38 -p1 -b .rh448904
%patch39 -p1 -b .rh461903

# No, I don't know what this is doing in the tarball.
rm -f rexec/rexec

%build
sh configure --with-c-compiler=gcc
%ifarch s390 s390x
%{__perl} -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -fPIC -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE,;
    s,^LDFLAGS=,LDFLAGS=-pie,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG
%else
%{__perl} -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -fpic -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE,;
    s,^LDFLAGS=,LDFLAGS=-pie,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG
%endif
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,5,8}
mkdir -p ${RPM_BUILD_ROOT}/etc/pam.d

make INSTALLROOT=${RPM_BUILD_ROOT} BINDIR=%{_bindir} MANDIR=%{_mandir} install

install -m 644 %SOURCE1 ${RPM_BUILD_ROOT}/etc/pam.d/rexec
install -m 644 %SOURCE2 ${RPM_BUILD_ROOT}/etc/pam.d/rlogin
install -m 644 %SOURCE3 ${RPM_BUILD_ROOT}/etc/pam.d/rsh

mkdir -p ${RPM_BUILD_ROOT}/etc/xinetd.d/
install -m644 %SOURCE5 ${RPM_BUILD_ROOT}/etc/xinetd.d/rsh
install -m644 %SOURCE6 ${RPM_BUILD_ROOT}/etc/xinetd.d/rlogin
install -m644 %SOURCE7 ${RPM_BUILD_ROOT}/etc/xinetd.d/rexec

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc README BUGS
%attr(4755,root,root)	%{_bindir}/rcp
%{_bindir}/rexec
%attr(4755,root,root)	%{_bindir}/rlogin
%attr(4755,root,root)	%{_bindir}/rsh
%{_mandir}/man1/*.1*

%files server
%defattr(-,root,root,-)
%config(noreplace) /etc/pam.d/rsh
%config(noreplace) /etc/pam.d/rlogin
%config(noreplace) /etc/pam.d/rexec
%{_sbindir}/in.rexecd
%{_sbindir}/in.rlogind
%{_sbindir}/in.rshd
%config(noreplace) /etc/xinetd.d/*
%{_mandir}/man8/*.8*

%changelog
* Tue Feb 09 2010 Adam Tkac <atkac redhat com> - 0.17-60
- merge review related fixes (#226379)
- remove unused patches
  - netkit-rsh-0.16-pamfix.patch
  - netkit-rsh-0.16-jbj2.patch
  - netkit-rsh-0.16-jbj3.patch

* Wed Jan 13 2010 Adam Tkac <atkac redhat com> - 0.17-59
- rebuild against new audit

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 0.17-58
- use password-auth common PAM configuration instead of system-auth

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.17-57
- rebuilt with new audit

* Tue Aug 11 2009 Adam Tkac <atkac redhat com> 0.17-56
- remove URL from rexec source, it is no longer publicly available

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 30 2009 Adam Tkac <atkac redhat com> 0.17-54
- improve pam_env patch

* Thu Mar 26 2009 Adam Tkac <atkac redhat com> 0.17-53
- check return value from close to catch errors on NFS filesystems (#461903)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 03 2008 Adam Tkac <atkac redhat com> 0.17-51
- updated ipv6 patch due rpm 4.6 (#465053)
- make in.rshd working on kernels without audit support (#448904)

* Fri May 09 2008 Adam Tkac <atkac redhat com> 0.17-50
- fixed typos in arg_max and audit patches (#445606)
- use pam_rhosts, not pam_rhosts_auth (#445606)

* Mon Apr 14 2008 Adam Tkac <atkac redhat com> 0.17-49
- use sysconf for ARG_MAX value (#440867)

* Thu Mar 27 2008 Adam Tkac <atkac redhat com> 0.17-48
- in.rexecd username limit was 14 characters, not 16

* Tue Mar 25 2008 Adam Tkac <atkac redhat com> 0.17-47
- fixed NULL pointer dereference (#437815)
- cleanup in audit patch

* Thu Feb 14 2008 Adam Tkac <atkac redhat com> 0.17-46
- rebuild with gcc4.3
- build with -D_GNU_SOURCE

* Sat Oct 20 2007 Steve Grubb <sgrubb@redhat.com> 0.17-45
- update for audit

* Tue Oct 16 2007 Adam Tkac <atkac redhat com> 0.17-44
- added -D option for compatibility with F8 test releases
- fixed rsh-server description

* Thu Sep 27 2007 Adam Tkac <atkac redhat com> 0.17-43
- removed -D option from rshd and rlogind (we have -a option when
  we need force reverse DNS lookup)
- patches netkit-rsh-0.17-nodns.patch and netkit-rsh-0.17-nohostcheck.patch
  are substituted by netkit-rsh-0.17-dns.patch

* Wed Aug 22 2007 Adam Tkac <atkac redhat com> 0.17-42
- rebuild (BuildID feature)

* Wed Jul 26 2007 Adam Tkac <atkac redhat com> 0.17-41
- improved nodns patch (in.rshd also has -D option now)

* Tue Apr 10 2007 Adam Tkac <atkac redhat com> 0.17-40
- improved -D option to rlogind - when name won't be resolved rlogind uses IP address
- added smp_mflags to make

* Mon Jan 22 2007 Adam Tkac <atkac redhat com> 0.17-39
- rebased on ncurses instead of libtermcap

* Tue Dec 05 2006 Adam Tkac <atkac redhat com> 0.17-38
- rsh now load pan_env module correctly

* Tue Oct 24 2006 Adam Tkac <atkac@redhat.com> 0.17-37
- added xinetd dependency to rsh-server

* Wed Oct  4 2006 Karel Zak <kzak@redhat.com> 0.17-36
- fix #209277 - rsh-server not linked to PAM (missing BuildRequires)

* Tue Jul 17 2006 Karel Zak <kzak@redhat.com> 0.17-35
- added support for IPv6 (patch by Jan Pazdziora)
- fix #198632 - add keyinit instructions to the rsh, rlogin and rexec PAM scripts
  (patch by David Howells)
- fix #191390 - improve linefeed patch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.17-34.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.17-34.1
- bump again for double-long bug on ppc(64)

* Thu Feb  9 2006 Karel Zak <kzak@redhat.com> 0.17-34
- fix #178916 - Line feeds when password needs changing with rlogin

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 0.17-33.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0.17-33.1
- rebuilt

* Mon Nov 28 2005 Karel Zak <kzak@redhat.com> 0.17-33
- fix #174146 - pam_access.so does not work with rexecd

* Thu Nov 24 2005 Karel Zak <kzak@redhat.com> 0.17-32
- fix #174045 - rcp outputs negative file size when over 2GB

* Thu Oct 13 2005 Karel Zak <kzak@redhat.com> 0.17-31
- rewrite rexecd PAM_conversation()

* Thu Oct 13 2005 Karel Zak <kzak@redhat.com> 0.17-30
- replace pam_stack with "include"

* Sat Mar  5 2005 Karel Zak <kzak@redhat.com> 0.17-29
- rebuilt

* Thu Feb  3 2005 Karel Zak <kzak@redhat.com> 0.17-28
- malicious rcp server can cause rcp to write to arbitrary files (like scp CAN-2004-0175) (#146464)

* Mon Dec  6 2004 Karel Zak <kzak@redhat.com> 0.17-27
- removed BSD stuff "signal(SIGCHLD, SIG_IGN)". It's unsupported by POSIX/linux. (#122315)

* Sat Dec  4 2004 Karel Zak <kzak@redhat.com> 0.17-26
- "-D" option turns off reverse DNS in rexecd (#135827)

* Wed Nov 17 2004 Karel Zak <kzak@redhat.com> 0.17-25
- rexecd uses PAM session now (#68590)
- fixed errno usage in rcp (#67361)
- fixed rexec fails with "Invalid Argument" (#118630)

* Mon Oct 18 2004 Radek Vokal <rvokal@redhat.com> 0.17-24
- The username and password for ~/.netrc are used (#135643)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 12 2004 Phil Knirsch <pknirsch@redhat.com> 0.17-22
- Added all other tools to list of PIE enabled apps.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb  5 2004 Thomas Woerner <twoerner@redhat.com> 0.17-20
- in.rexecd, in.rlogind and in.rshd are pie, now

* Tue Oct 21 2003 Phil Knirsch <pknirsch@redhat.com> 0.17-19
- Included updated patch from #105733.

* Thu Oct 02 2003 Phil Knirsch <pknirsch@redhat.com> 0.17-18
- Fixed YAT (#79391).
- Included feature request #105733 (-D option).

* Fri Jun 27 2003 Phil Knirsch <pknirsch@redhat.com> 0.17-17.1
- rebuilt

* Thu Jun 26 2003 Phil Knirsch <pknirsch@redhat.com> 0.17-17
- Included chdir patch (#57392).
- Included pam-nologin patch (#63806).

* Tue Jun 17 2003 Phil Knirsch <pknirsch@redhat.com> 0.17-16
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 0.17-15
- rebuilt

* Tue May 06 2003 Phil Knirsch <pknirsch@redhat.com>
- Fixed manpages (#7168).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan 17 2003 Phil Knirsch <pknirsch@redhat.com> 0.17-13
- Added LFS support (#67362).
- Fixed user and host patch (#80822).

* Tue Jan 14 2003 Phil Knirsch <pknirsch@redhat.com> 0.17-12
- Fixed bug #79391 (typo in description).

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 0.17-11
- remove directory names from PAM configuration files, allowing them to be used
  for all arches on multilib systems

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 0.17-9
- Don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 30 2002 Phil Knirsch <pknirsch@redhat.com>
- Bumped version for rebuild
- Added the remote user and host addition (RFE #42880)

* Tue Jul 24 2001 Phil Knirsch <pknirsch@redhat.com>
- Fixed really missing BuildPrereq: libtermcap-devel (#49577)
- Fixed security problem with rexec.pam (#49181)

* Fri Jun 22 2001 Phil Knirsch <pknirsch@redhat.com>
- Update to latest stable version 0.17
- Removed unneeded glib22 patch

* Mon Apr 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- tag xinetd config files as config files

* Wed Apr  4 2001 Jakub Jelinek <jakub@redhat.com>
- don't let configure to guess compiler, it can pick up egcs

* Mon Feb  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- securetty is screwy because rsh doesn't allocate one and rlogin does auth
  before it has a tty, so change the hard-coded TTYs used from "tty" for all
  to "rsh" or "rlogin" or "rexec"

* Tue Oct 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix PAM config files to always honor nologin and securetty, to use rhosts,
  and to fall back to password auth only for rlogin and rexec (#17183)
- add references to pam_env to the PAM configs as well (#16170)
- disable rlogin and rsh by default

* Mon Oct 02 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix typo in the rexec xinetd configuration file (#18107)

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix typo in the rlogin PAM config file
- continue the tradition of messed-up release numbers

* Tue Jul 18 2000 Bill Nottingham <notting@redhat.com>
- add description & default to xinetd file

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- update to 0.17.

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify PAM setup to use system-auth

* Mon May 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- expunge all mentions of kerberos authentication or DES encryption using
  kerberos from the man pages

* Thu May 25 2000 Trond Eivind Glomsrod <teg@redhat.com>
- switched to xinetd

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Fri Mar 04 2000 Nalin Dahyabhai <nalin@redhat.com>
- make rlogin still work correctly when argv[0] = "rsh"

* Mon Feb 28 2000 Jeff Johnson <jbj@redhat.com>
- workaround (by explicitly prompting for password) #4328 and #9715.

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- mark pam config files as %%config.

* Fri Feb  4 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Sun Jan 30 2000 Bill Nottingham <notting@redhat.com>
- remove bogus rexec binary when building; it causes weirdness

* Fri Jan 28 2000 Jeff Johnson <jbj@redhat.com>
- Make sure that rshd is compiled with -DUSE_PAM.

* Mon Jan 10 2000 Jeff Johnson <jbj@redhat.com>
- Fix bug in rshd (hangs forever with zombie offspring) (#8313).

* Wed Jan  5 2000 Jeff Johnson <jbj@redhat.com>
- fix the PAM fix yet again (#8133).

* Tue Jan  4 2000 Bill Nottingham <notting@redhat.com>
- split client and server

* Tue Dec 21 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.16.
- dup setuid bits into files list.

* Fri Jul 30 1999 Jeff Johnson <jbj@redhat.com>
- update to rexec-1.5 client (#4262)

* Wed May 19 1999 Jeff Johnson <jbj@redhat.com>
- fix broken rexec protocol in in.rexecd (#2318).

* Tue May  4 1999 Justin Vallon <vallon@mindspring.com>
- rcp with error was tricked by stdarg side effect (#2300)

* Thu Apr 15 1999 Michael K. Johnson <johnsonm@redhat.com>
- rlogin pam file was missing comment magic

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip rexec

* Fri Mar 26 1999 Jeff Johnson <jbj@redhat.com>
- rexec needs pam_set_item() (#60).
- clarify protocol in rexecd.8.
- add rexec client from contrib.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 14 1998 Erik Troan <ewt@redhat.com>
- built against new ncurses

* Sat Apr  5 1998 Marcelo F. Vianna <m-vianna@usa.net>
- Packaged for RH5.0 (Hurricane)

* Tue Oct 14 1997 Michael K. Johnson <johnsonm@redhat.com>
- new pam conventions

* Tue Jul 15 1997 Erik Troan <ewt@redhat.com>
- initial build
