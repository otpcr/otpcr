|

**NAME**

    ``GENOCIDE`` - Since 4 March 2019.


**SYNOPSIS**

    ``genocide`` [-h] [-a] [-c] [-d] [-l LEVEL] [-m MODS] [-n] [-s] [-v] [-w] [-u] [--wdr WDR]
    
    | ``genocide <cmd> [key=val] [key==val]``
    | ``genocide -cvaw [mods=mod1,mod2]``
    |

**DESCRIPTION**

    ``GENOCIDE`` holds evidence that king
    netherlands is doing a genocide, a
    :ref:`written response <king>` where king
    netherlands confirmed taking note
    of “what i have written”, namely
    :ref:`proof  <evidence>` that medicine
    he uses in treatment laws like zyprexa,
    haldol, abilify and clozapine are not medicine
    but poison.

    Poison that makes impotent, is both
    physical (contracted muscles) and
    mental (make people hallucinate)
    torture and kills members of the
    victim groups: Elderly, Handicapped, Criminals
    and Psychiatric patients.

    ``GENOCIDE`` contains :ref:`correspondence
    <writing>` with the International Criminal
    Court, asking for arrest of the king of the
    netherlands, for the genocide he is committing
    with his new treatment laws.

    Current status is a :ref:`"no basis to proceed"
    <writing>` judgement of the prosecutor which
    requires a :ref:`"basis to prosecute" <reconsider>`
    to have the king actually arrested.


**INSTALL**


    * installation is done with pipx

    | ``$ pipx install genocide``
    | ``$ pipx ensurepath``
    |
    | <new terminal>
    |
    | ``$ genocide srv > genocide.service``
    | ``$ sudo mv genocide.service /etc/systemd/system/``
    | ``$ sudo systemctl enable genocide --now``
    |
    | joins ``#genocide`` on localhost
    |


**USAGE**


    * use ``genocide`` to control the program, default it does nothing

    | ``$ genocide``
    | ``$``
    |

    * the -h option will show you possible options

    |
    | ``$ genocide -h``
    |

    .. list-table::
      :align: left

      * - Options
        - Description

      * - -h, --help
        - show this help message and exit
      * - -a, --all
        - load all modules.
      * - -c, --console
        - start console.
      * - -d, --daemon
        - start background daemon.
      * - -i, --ignore IGNORE
        -  modules to ignore.
      * - -l, --level LEVEL
        -  set loglevel.
      * - -m, --mods MODS
        - modules to load.
      * - -n, --index INDEX
        - set index to use.
      * - -r, --read
        - read modules on start.
      * - -s, --service
        - start service.
      * - -v, --verbose
        - enable verbose.
      * - -w, --wait
        - wait for services to start.
      * - -u, --user
        - use local mods directory.
      * - -x, --admin
        - enable admin mode.
      * - --wdr WDR
        - set working directory.
      * - --nochdir
        - set working directory.


    * see list of commands
    
    | ``$ genocide cmd``
    | ``atr,cfg,cmd,dis,dne,dpl,err,exp,fie,flt,fnd,imp,``
    | ``log,lou,man,mod,nme,now,pth,pwd,rem,req,res,rss,``
    | ``sil,slg,srv,syn,tbl,tdo,thr,tmr,upt,ver,wdr``
    |

    * start console

    | ``$ genocide -c``
    |

    * start console and run irc and rss clients

    | ``$ genocide -c mods=irc,rss``
    |

    * list available modules

    | ``$ genocide mod``
    | ``adm,bsc,cfg,fie,flt,fnd,irc,log,man,mbx,mdl,pth,pwd``
    | ``req,rss,rst,sil,slg,tbl,tdo,thr,tmr,udp,wdr,web,wsd``
    |

    * start daemon

    | ``$ genocide -d``
    | ``$``
    |

    * start service

    | ``$ genocide -s``
    | ``<runs until ctrl-c>``
    |


**COMMANDS**

    * here is a list of available commands

    | ``atr`` - show attributes
    | ``cfg`` - irc configuration
    | ``cmd`` - commands
    | ``dis`` - show deaths by disease
    | ``dne`` - flag a todo as done
    | ``dpl`` - sets display items
    | ``eml`` - show emails
    | ``err`` - show errors
    | ``exp`` - export opml (stdout)
    | ``fie`` - show fields of an object
    | ``flt`` - show bots in fleet
    | ``fnd`` - locate objects
    | ``imp`` - import opml
    | ``log`` - log text
    | ``lou`` - enable loud mode
    | ``man`` - create manual page
    | ``mbx`` - import mailbox
    | ``mod`` - show available modules
    | ``nme`` - set name of a feed
    | ``now`` - show genocide stats of today
    | ``pth`` - show path to website on disk
    | ``pwd`` - sasl nickserv name/pass
    | ``rem`` - removes a rss feed
    | ``req`` - request to the prosecutor
    | ``res`` - restore objects
    | ``rss`` - add a feed
    | ``sil`` - enable silent mode
    | ``syn`` - sync rss feeds
    | ``tbl`` - create table module
    | ``tdo`` - add todo item
    | ``thr`` - show running threads
    | ``tmr`` - timers
    | ``udp`` - send udp packet to udp/irc relay
    | ``upt`` - show uptime
    | ``ver`` - version
    | ``wdr`` - show working directory
    | ``wsd`` - show wisdom
    |

**CONFIGURATION**


    * irc

    | ``$ genocide cfg irc server=<server>``
    | ``$ genocide cfg irc hannel=<channel>``
    | ``$ genocide cfg irc nick=<nick>``
    |

    * sasl

    | ``$ genocide pwd <nsnick> <nspass>``
    | ``$ genocide cfg irc password=<frompwd>``
    |

    * rss

    | ``$ genocide rss <url>``
    | ``$ genocide dpl <url> <item1,item2>``
    | ``$ genocide rem <url>``
    | ``$ genocide nme <url> <name>``
    |

    * opml

    | ``$ genocide exp``
    | ``$ genocide imp <filename>``
    |


**PROGRAMMING**

    genocide has it's user modules in the ~/.genocide/mods directory so for a
    hello world command you would  edit a file in ~/.genocide/mods/hello.py
    and add the following
    
    ::

        def hello(event):
            event.reply("hello world !!")


    typing the hello command would result into a nice hello world !!
    

    ::

        $ genocide hello
        hello world !!


    commands run in their own thread and the program borks on exit to enable a
    short debug cycle, output gets flushed on print so exceptions appear in the
    systemd logs. modules can contain your own written python3 code.
    

**SOURCE**

    source is at `https://github.com/bthate/genocide <https://github.com/bthate/genocide>`_
    

**FILES**

    | ``~/.genocide``
    | ``~/.local/bin/genocide``
    | ``~/.local/share/pipx/venvs/genocide/*``
    |

**AUTHOR**

    ``Bart Thate`` <``bthate@dds.nl``>
    

**COPYRIGHT**

    ``GENOCIDE`` is Public Domain.
