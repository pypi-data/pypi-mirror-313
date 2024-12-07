# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini(at)gmail.com
# ---------------------------------------------------------------------------------------------------------------
import platform
import sys
import os
import pprint

from piwiPre.pwpActor import ACTOR
from piwiPre.pwpErrors import LOGGER
from piwiPre.pwpArgsIni import PwpArgsIni, ConstraintHow, CVS, ServerSetup, PwpArgType


class PwpParser(PwpArgsIni):
    default_ini_file = "piwiPre.ini"

    def __init__(self, arguments=None, with_config=True, program: str = "piwiPre", parse_args=True, piwi_pre=None):
        super().__init__()
        self.config = None  # the config after parsing HOME & BASE ini files and cmdline args
        self.cmd_line_args = arguments if arguments else []
        self.piwi_pre = piwi_pre
        self.add_header("""
.. _configuration:
        
Commandline Flags and configuration items
#########################################

French version:  :ref:`configuration_fr`

This file is the configuration of piwiPre for the enclosing directory

Unless stated otherwise, the  configuration items have a command line argument counterpart,
with the same name, starting with - - .

The default value is given as an argument.

The configuration file uses the yaml syntax,
and uses pyYaml  to read/write the configuration file

- *boolean* values are *true* and *false*
- *None* denotes a value which is not set. The previous value in the ini file hierarchy is inherited.
- *string* SHOULD single or double quotes to prevent yaml from interpreting values.
- *''* and *""* denote an empty value, which is different from a value absent and inherited
- *directory* should be a valid path syntax (absolute or relative), written as a string.
- *dictionary* read key : value
""")
        self.add_header("""
.. _configuration_fr:

Options de ligne de commande et éléments de configuration
##########################################################

English version:  :ref:`configuration`

Ce fichier est la configuration de piwiPre pour un dossier

Sauf lorsque indiqué autrement, les éléments de configuration ont une contrepartie sur la ligne de commande,
avec le même nom, mais commençant par - - .

La valeur par défaut est indiquée plus bas.

Le fichier de configuration utilise la syntaxe de YAML,
et piwiPre utilise pyYaml pour lire/écrire la configuration.

- les valeurs *booléennes*   sont *true* et *false* (vrai et faux)
- *None* dénote une valeur qui n'est pas positionnée, la valeur précédente dans la hiérarchie des .ini est héritée.
- *string* DOIT être une chaîne de caractères délimitée par les caractères ' ou \"
- *''* ou *""* est une chaîne vide, ce qui est différent d'une valeur absente
- *directory* doit être une syntaxe de chemin valide (absolu ou relatif), écrit comme une chaîne.
- un dictionnaire (*dictionary*) s'écrit: clef : valeur         
        """, lang='fr')

        self.add_header("""
.. _fr_configuration:

Configuration hierarchy
=======================

1. Default values are set for all items.
   Subsequent configuration data is read from files named 'piwiPre.ini'

2. piwiPre manages the part of cmd-line items that would globally change the behavior,
   (other cmd-line flags are managed afterwards)
   i.e:

    - --home and --base : the change the .ini read     
    - --version, --help, --full-help, --licence, --dump-config : they stop pwiPre once their action is done

   
3. In the user HOME directory, as a special case, '.piwiPre.ini' is read instead.
   If it exists, it is the first configuration file read.
   If it exists, it is the first configuration file read.add
   
   This file should be protected against reading from others,
   (chmod 500 in the Linux case).
   It is used to store confidential information:

   - SSH information : ssh-user, ssh-host, ssh-port
   - NB: SSH password is stored differently see :ref:`ssh`
   - SQL information: sql-host, sql-port, sql-user, sql-password
   - piwigo information: piwigo-user
   
   This file also typically stores **default** directories for the user:

   - triage, album, thumbnails, album-config
   - remote-thumbnails and enable-remote-thumbnails

   Other global configuration items could also be stored there:
   
   - month-name, copyright, instructions, names, authors, dates
  
  The location of HOME can be changed with --home
   
4. in BASE. 

   This BASE/piwiPre.ini should store **non-default** directories and information, 
   that are specific to this particular directory
   
   So, if the user wants to maintain various settings, this can be done in a per directory basis,
   
   For instance one directory with 1 naming convention and another directory for a different naming
   Here, one usually  sets up the global configuration without the confidential information
   and without details specific to each TRIAGE directory.
   
   If this file stores confidential information, it should also be chmod 500.
   
   CAVEAT: Once BASE/piwiPre.ini has been read, new values of the confidential configuration 
   are no more taken into account.

5. On cmdLine. When used on the command-line, options start with '--', such as '--version' etc.

    NB: --base and --home change the default configuration files that are read BEFORE the command-line.
    so, as a special case, these items are taken into account at the start of piwiPre.
 
6. When managing TRIAGE, in TRIAGE subdirectories. 

   These .ini files are read only when processing files in TRIAGE.
   Only directory-specific configuration should be stored here.
   
   To clarify a difficulty: when managing TRIAGE, the configuration files in AUTO-CONFIG are *not* read
     
   Typically, one stores there 'names', 'authors', 'dates', 'copyright', 'instructions',
   if some of these should be different for a specific directory.
   
   If enable-auto-configuration is true, this file will be copied in the corresponding AUTO-CONFIG directory
   
   If there was a preexisting .ini file in the AUTO-CONFIG subdir, then it is clobbered by the new one.
   

7. When verifying ALBUM, in the directory hierarchy of AUTO-CONFIG.

   These .ini files are read only when processing files in ALBUM.
   
   .ini files in AUTO-CONFIG are usually a copy of an .ini file in the original TRIAGE directory, but they *can* be
   hand-writen by the piwigo administrator.
    
   To clarify a difficulty: when managing ALBUM, the configuration files in TRIAGE are *not* read
    
   For instance, some sub-dire of ALBUM may hold pictures without shooting date in the Exif data,
   therefore the naming method is different.
   
NB 1: The later has precedence over the sooner.
 
NB 2: Therefore, cmdLine items do not modify configuration options found in directories of TRIAGE and AUTO-CONFIG.
   
   The only way to reset these are:
   
   - To modify the .ini files in TRIAGE, and then run piwiPre to forward the modifications to AUTO-CONFIG
   - To edit .ini files in AUTO-CONFIG 
   
.. attention::

   piwiPre.ini and HOME/.piwiPre.ini should be written with UTF8 encoding

""")

        self.add_header("""

Hiérarchie des configurations
=============================

La configuration de piwiPre est calculée dans l'ordre suivant:

1) Chaque item de configuration se voit attribuer sa valeur par défaut, telle qu'indiquée ici.

   Les configurations suivantes seront lues dans des fichiers nommés 'piwiPre.ini', 

2) piwiPre gère les élements de la ligne de commande qui modifient son fonctionnement de façon globale,
   (les autres éléments seront traités ensuite). C'est à dire:
   
    - --home and --base : ils changent la séquence de .ini lus par la suite     
    - --version, --help, --full-help, --licence, --dump-config : ils arrêtent piwiPre une fois qu'ils ont été traités.
   
3) Dans le dossier personnel de l'utilisateur (HOME), c'est le fichier .piwiPre.ini qui est lu. 
   noter le '.' initial, qui dénote un fichier 'caché'
   
   Ce fichier DOIT être protégé contre la lecture par d'autres personnes que son propriétaire 
   (l'équivalent de chmod 500 pour le cas linux), car il contient des informations confidentielles:
   
   - sql-host sql-port sql-user sql-pwd
   - ssh-host ssh-port  ssh-user ssh-incoming
   - piwigo-user 
  
   D'autres éléments de configuration peuvent aussi être stockés dans HOME/.piwiPre.ini.

   L'emplacement de HOME peut être changé avec l'option ---home
   
4. Dans BASE, c'est à dire le dossier d'où est lancé piwiPre.

   Ici, on mets habituellement en place la configuration globale pour un album racine particulier, sans les 
   informations confidentielles qui sont dans HOME, et sans les détails spécifique à chaque sous-dossier de TRIAGE.
   
   Donc ce fichier est en général vide quand n seul album racine ('photo', par défaut) est utilisé.
   
   Si ce dossier contient des informations confidentielles 
   (par exemple dans un cas où un album racine n'est pas accédé de la même façon que les autres)
   il doit alors, lui aussi, être protégé en lecture (chmod 500)
   
   Une fois que cqd/piwiPre.ini a été lu, aucune autre information confidentielle supplémentaire ne sera prise en compte
   
5. Sur la ligne de commande. Dans ce cas, les options suivent l'usage Linux, et commencent donc par '--', 
   par exemple '--help'
   
6. lorsque on importe des photos, (et donc TRIAGE est défini, et verify-album non défini), 
   dans chacun des sous-dossier de TRIAGE.
   
   Ces fichiers .ini ne sont lu qu'en cas d'importation, c'est-à-dire ne sont pas lus 
   lorsque verify-album est défini.
   
   Typiquement, on va stocker dans ces fichiers des valeurs spécifiques au dossier pour 
   ‘names’, ‘authors’, ‘dates’, ‘copyright’, ‘instructions’. Le .ini sera alors recopié dans le sous-repertoire de
   THUMBNAILS pour que ces valeurs soient aussi utilisées lors d'une phase de vérification des albums.
   
   Si un fichier .ini était présent dans le sous-repertoire de THUMBNAILS il sera écrasé par le nouveau.

7. Lorsque on vérifie les albums, c'est à dire lorsque verify-album est défini, dans la hiérarchie de AUTO-CONFIG.

   Ces .ini peuvent avoir été générés automatiquement à travers enable-auto-configuration, 
   ou bien avoir été écrits manuellement par l'administrateur.
   
   Clarifions un point: quand on gère les albums, les fichiers de configuration dans TRIAGE ne sont *pas* lus.
    
   ces fichiers .ini sont utilisés typiquement pour maintenir des élements de configuration spécifiques aux sous-albums 
   
   Par exemple, un sous-album peut contenir des photos qui n'ont pas de meta-données de date, 
   et donc la methode de gestion de dates est spécifique.


Dans cette hiérarchie de configuration, les dernières étapes ont précédence sur les premières.
Donc les seules façons de changer un .ini dans AUTO-CONFIG sont de:

- exécuter une importation de fichier, avec un nouveau .ini dans TRIAGE
- modifier à la main le .ini dans AUTO-CONFIG

       
        """, lang='fr')

        self.add_header("""
Some vocabulary
===============

- The **piwigo host** is the server where the piwigo service runs. 
  Usually this is a cloud-based host, or a NAS, or a Linux server.

- The **piwiPre host** is the computer where piwiPre runs. 
  Usually this is a desktop PC, running Linux or Windows, but could be also the same machine than piwigo host.

- **HOME** is the is the user personal directory,
  ie c:\\users\\{username} for Windows and /home/{username} for linux
  The default value for HOME is read from the environment variables, but can be changed.
  
- **BASE** is the directory where piwiPre is run. If a relative path is used, then it starts from there. 
  For instance, 'album: ALBUM' specifies that the current album directory is BASE/ALBUM
  
  The default value for BASE is HOME/Pictures/BASE,  
""")

        self.add_header("""
Vocabulaire
===========

- l'**hôte piwigo** est le serveur sur lequel le service piwigo tourne. 
  En général, c'est un serveur dans le cloud, ou un NAS, ou un serveur Linux domestique.
  
- l'**hôte piwiPre** est le calculateur sur lequel piwiPre tourne.
  En général, c'est un PC personnel, sous Windows ou Linux, mais ce pourrait aussi être la même machine
  que l'hôte piwigo.
  
- **HOME** est le dossier personnel de l'utilisateur, c'est à dire
  c:\\users\\{username} pour Windows and /home/{username} pour linux.
  La valeur par défaut de HOME est lue dans les variables environnement, mais peut être changée.
  
- **BASE** est le dossier dans lequel piwiPre s'exécute. 
  Lorsqu'un chemin relatif est spécifié, il est relatif par rapport à BASE.
  Par exemple "album: ALBUM' spécifie que l'album courant est BASE/ALBUM""", lang='fr')

        # ------------------------------------------------------------------------------------------------------
        # Management of directories
        # ------------------------------------------------------------------------------------------------------

        self.add_header("""
Management of directories
=========================""")

        self.add_header("""
Gestion des dossiers
=======================""", lang='fr')

        self.add_item('triage',
                      help='directory where are stored incoming pictures/videos.',
                      fr_help="dossier des images/vidéo à importer",
                      action='store',
                      default='TRIAGE',
                      pwp_type=PwpArgType.DIR,
                      setups=[ServerSetup(pwp_type=PwpArgType.DIR)],
                      config="""
- value = 'directory': Sets the TRIAGE directory

  This directory is read-only
  
  This directory CAN be erased by user once processing is finished.

- value = None: no TRIAGE directory to process
  
  When verify-album is used, triage is automatically set to None in order to avoid confusion 
  between the configurations of triage and album. a Warning is issued.
  
""",
                      fr_config="""
- valeur = 'dossier': Indique le dossier d'où trier puis importer des images/vidéos

  Ce dossier est en lecture seule, et PEUT être éffacé par l'utilisateur quand le piwiPre à terminé
  
- valeur = None: il n'y a pas de dossier de tri, et donc pas d'image à importer

  Quand verify-album est utilisé, triage est automatiquement positionné à None de façon à éviter la confusion   
  entre les configurations triage et album. Un warning est généré.
""")

        self.add_item('album',
                      help='directory where piwigo pictures are stored after processing.',
                      fr_help="dossier où les images sont stockées après traitement",
                      action='store',
                      default='ALBUM',
                      pwp_type=PwpArgType.DIR,
                      setups=[ServerSetup(pwp_type=PwpArgType.DIR)],
                      config="""
- value = 'directory' : Sets root directory for ALBUM
 
  a typical value is //NAS/photo, when this directory is synchronized with the piwigo repository 
  
  another typical value is ALBUM, when the piwigo repository is not accessible
  
- value =  None, the ALBUM directory is not managed, files are not copied from TRIAGE to ALBUM.""",

                      fr_config="""
- valeur = 'dossier': Indique le dossier où seront posées les images/vidéos

  une valeur typique est //NAS/photo, si ce dossier est synchronisé avec le stockage de piwigo
  
  une autre valeur typique est ALBUM, si le stockage de piwigo n'est pas accessible   
  
- valeur = None: il n'y a pas de dossier pour poser les images, et donc les images ne seront pas importées                      
""")

        self.add_item('auto-config',
                      help='directory ALBUM configuration is automatically stored after processing.',
                      fr_help="dossier où les configurations d'ALBUM sont stockées après traitement",
                      action='store',
                      default='AUTO-CONFIG',
                      pwp_type=PwpArgType.DIR,
                      setups=[ServerSetup(pwp_type=PwpArgType.DIR)])

        self.add_item('thumbnails',
                      help='Directory for piwigo thumbnails.',
                      fr_help="dossier pour les miniatures (thumbnail) de piwigo",
                      action='store',
                      default='THUMBNAILS',
                      pwp_type=PwpArgType.DIR,
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, album=CVS.ALL,
                                          how=ConstraintHow.FORCED, value=""),
                              ServerSetup(pwp_type=PwpArgType.DIR)],
                      config="""
- value = 'directory' : Sets the thumbnails directory.

  the typical value when the thumbnails directory is local : THUMBNAILS
  a typical value is '//NAS/web/piwigo/_data/i/galleries/photo', appropriate for synology NAS
""",
                      fr_config="""
- valeur = 'dossier' : le dossier racine pour les miniatures

  Une valeur typique quand le dossier est local : THUMBNAILS
  
  Une valeur typique pour les NAS Synology est '//NAS/web/piwigo/_data/i/galleries/photo'      
""")

        self.add_item('backup',
                      help='Directory where modified files are saved.',
                      fr_help="dossier où sont sauvegardés le fichiers modifiés.",
                      action='store',
                      default='BACKUP',
                      pwp_type=PwpArgType.DIR,
                      setups=[ServerSetup(pwp_type=PwpArgType.DIR)],
                      config="""
        - value = 'directory' : Sets the BACKUP directory, where backup-ed files are saved before any modification.

          This directory can be erased by the user once processing is finished.
          """,
                      fr_config="""
        - valeur = 'dossier' : là où sont sauvegardés les fichiers à sauvegarder

          Ce dossier PEUT être effacé par l'utilisateur lorsque piwiPre a terminé.      
        """)

        self.add_item('backup-test-stamp',
                      help='FOR TEST ONLY, set the backup time stamp',
                      fr_help="POUR TEST SEULEMENT, l'horodatage du backup",
                      action='store',
                      location='args',
                      default="",
                      pwp_type=PwpArgType.STR)

        self.add_item('remote-thumbnails',
                      help='Directory for piwigo thumbnails, on REMOTE piwigo host.',
                      fr_help="dossier DISTANT (c-à-d sur le serveur piwigo) pour les miniatures",
                      action='store',
                      pwp_type=PwpArgType.STR,
                      default="",
                      setups=[ServerSetup(album=CVS.ALL, thumbnails=CVS.REMOTE,
                                          how=ConstraintHow.VALUE,
                                          value='/volume1/web/piwigo/_data/i/galleries/photo',),
                              ServerSetup(album=CVS.ALL, thumbnails=CVS.UNUSED,
                                          how=ConstraintHow.FORCED,
                                          value="", ),
                              ServerSetup(),],
                      config="""
This is useful ONLY when there is NO direct access to the piwigo thumbnails, in this case, THUMBNAILS will be used
as a cache before sftp transfert.
                      
- value = 'directory' : Sets the thumbnails directory when accessed through ssh/sftp on the remote host
- if value is None, then piwigo thumbnails are NOT accessed through sftp

a typical value is '/volume1/web/piwigo/_data/i/galleries/photo', appropriate for synology NAS 
""",
                      fr_config="""
Ceci n'est utile que lorsqu'il n'y a PAS d'accès direct au stockage des miniatures. 
Dans ce cas, THUMBNAILS sera utilisé comme un cache avant le transfert via sftp.

- valeur = 'dossier' : le dossier DISTANT pour les miniatures
- valeur = None: il n'y a pas d'accès en sftp

Une valeur typique pour les NAS Synology est '/volume1/web/piwigo/_data/i/galleries/photo'                      
""")

        self.add_item('remote-album',
                      help='REMOTE directory for piwigo albums.',
                      fr_help="dossier DISTANT (c-a-d sur le serveur piwigo) pour les photos",
                      action='store',
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(album=CVS.REMOTE, thumbnails=CVS.ALL,
                                          how=ConstraintHow.VALUE, value="/remote-server/photo"),
                              ServerSetup()],
                      default="",
                      )

        self.add_item('remote-auto-config',
                      help='REMOTE directory for album auto-config.',
                      fr_help="dossier DISTANT (c-a-d sur le serveur piwigo) pour les auto-config d'album",
                      action='store',
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(album=CVS.REMOTE, thumbnails=CVS.ALL,
                                          how=ConstraintHow.VALUE,
                                          value="/remote-server/auto-config"),
                              ServerSetup()],
                      default="",
                      )

        self.add_item('piwigo-album-name',
                      help="Root piwigo album managed. If empty, piwiPre will select the first album",
                      fr_help="Album racine de piwigo à gérer. Si vide, piwiPre sélectionne le 1er album",
                      action="store",
                      default="",
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup()],
                      config="""
This item is useful only if enable-database is true.

piwiPre manages only one root piwigo album per execution (with all sub-albums),  
and MUST be coherent with the values of 'album' and 'thumbnails'

The list of first level albums can be seen through the piwigo administration web site
https://server-URL/piwigo/admin.php?page=albums

The default value is None. In this case, piwiPre will automatically select the first root album, 
which has the database global_rank "1"
        """,
                      fr_config="""
Cette valeur est utile seulement lorsque enable-database est 'true'

piwiPre gère uniquement 1 album piwigo racine (avec tous ses sous-albums) par utilisation
Cette valeur DOIT être cohérente avec les valeurs de 'album' et 'thumbnails'     

La liste des albums de 1e niveau peut être vue avec le site web d'administration de piwigo
https://server-URL/piwigo/admin.php?page=albums      

La valeur par défaut est None. Dans ce cas, piwiPre sélectionne automatiquement le 1e album racine,
qui a, dans la base de données, le global_rank 1        
        """)

        # ------------------------------------------------------------------------------------------------------
        # Global actions in ALBUM subdirectories
        # ------------------------------------------------------------------------------------------------------

        self.add_header("""
Global actions in ALBUM subdirectories
======================================
""")
        self.add_header("""
Actions globales sur les sous-dossiers de ALBUM
==================================================
        """, lang='fr')

        self.add_item('verify-album',
                      help='Directory in ALBUM to be verified',
                      fr_help="Repertoire de ALBUM à vérifier",
                      default="",
                      location='args',
                      pwp_type=PwpArgType.DIR,
                      setups=[ServerSetup(how=ConstraintHow.CMDLINE, pwp_type=PwpArgType.DIR, location='args')],
                      config="""

- Value = a directory in ALBUM to be verified
- Default : ''
- '{album}' is a special value, it means : album itself.
  so if --enable-verify-sub-album is true, everything is verified

If verify-album is set, triage is unset

Caveat: sub-directories of the target directory are NOT verified, 
unless --enable-verify-sub-album is true, which is not the default

Other useful flags with their typical value when verifying albums::

        --triage None
        --verify-album ALBUM/folder1 
        --restart-from-dir folder/sub-sub-dir      # (just in case this is necessary)
        --enable-verify-sub-album true             # useful only if folder1 or folder2 have sub-folders 
        --enable-thumbnails true                   # build thumbnails if they were not built
        --enable-thumbnails-delete true            # remove useless thumbnails
        --enable-metadata true                     # if metadata is lacking, will be set
        --enable-rotation true                     # rotate the pictures 
        --enable-database true                     # set in database
        --enable-conversion true                   # change pictures to jpg and video to mp4    

        --enable-metadata-reset false              # trust metadata that was generated previously
        --enable-date-in-filename true             # trust date that was generated previously 
        --enable-rename false                      # trust names that were generated previously
""",
                      fr_config="""
                      
 
- Valeur = un dossier de ALBUM à vérifier
- Défaut : ''
- '{album}' est une valeur spéciale, qui signifie : l'album racine

Si verify-album est true, alors la valeur de TRIAGE est annulée automatiquement

ATTENTION: les sous-répertoires ne sont pas vérifiés,
sauf si --enable-verify-sub-album true, ce qui n'est pas le défaut.

Autres options avec leurs valeur lorsque on utilise --verify-album::

     --triage None
     --verify-album ALBUM/folder1 
     --restart-from-dir folder/sub-sub-dir      # (au cas où ce soit nécessaire)
     --enable-verify-sub-album true             # utile seulement si folder1 a des sous-dossiers
     --enable-thumbnails true                   # construit les miniatures qui manquent
     --enable-thumbnails-delete true            # enlève les miniatures inutiles
     --enable-metadata true                     # rajoute les metadata manquantes
     --enable-rotation true                     # gère les rotations
     --enable-database true                     # insère dans la base de données piwigo
     --enable-conversion true                   # autorise la conversion des images en jpg et des video en mp4    

     --enable-metadata-reset false              # fait confiance aux metadata qui ont été générés précédemment
     --enable-date-in-filename true             # fait confiance aux dates qui ont été générés précédemment
     --enable-rename false                      # fait confiance aux noms de fichier qui ont été générés précédemment                     
                      """)

        self.add_item('enable-thumbnails-delete',
                      help='Enables deletion of useless piwigo thumbnails.',
                      fr_help="Autorise l'enlèvement des miniatures (thumbnails) piwigo inutiles",
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      default='true',
                      location='args',
                      setups=[ServerSetup(thumbnails=CVS.UNUSED,
                                          how=ConstraintHow.FORCED,
                                          value='false',
                                          pwp_type=PwpArgType.BOOL, ),
                              ServerSetup(pwp_type=PwpArgType.BOOL, ), ],
                      config="""
When doing verify-album  
this flag allows to remove thumbnails that are useless because there is no corresponding picture.

- It should be tested first with --dryrun
- For security, the default value is 'false': the user AS TO set explicitly to 'true'
        """,
                      fr_config="""
Dans une passe de vérification des albums (verify-album),
cette option autorise l'enlèvement des miniatures piwigo qui sont devenues obsolete car correspondant
à une image qui n'existe plus.

- Il est prudent de tester son effet avec --dryrun
- Par sécurité, sa valeur par défaut est 'false', l'utilisateur DOIT le positionner explicitement à 'true' 
""")

        # -------------------------------------------------------------------
        # Actions
        # -------------------------------------------------------------------

        self.add_header("""
Management of actions on pictures and videos
============================================

enable-XXX flags have 2 values:

- **false**: no action
- **true** : action is enabled if triage or album mode

By default, all actions are enabled, and this is typically done in the configuration files.


The default values enable a regular processing of ALBUM, provided **verify-album** is not empty.""")

        self.add_header("""
Gestion des actions sur les photos et les vidéos
================================================

les options enable-XXX ont 2 valeurs possibles:

- **false**: pas d'action
- **true** : l'action est autorisée 

Par défaut, toutes les actions sont autorisées, et ceci est changé généralement dans le fichier de configuration
dans HOME

Ces valeur par défaut sont compatibles avec les utilisations typiques,

- mode triage: trie renomme les photos/video et les envoies dans album
- mode vérification: l'album spécifié par **verify-album** est vérifié.""", lang='fr')

        self.add_item('enable-rename',
                      help='Enables files renaming',
                      fr_help="Autorise le renommage des fichiers",
                      action='store',
                      setups=[ServerSetup(pwp_type=PwpArgType.BOOL, value='true'), ],
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      default='true',
                      config="""

In album mode, pictures will **not** be moved from a directory to another, only the filename is changed""",
                      fr_config="""

En mode album, les fichiers ne sont **pas** changés de dossier, uniquement le nom de fichier est modifié
        """)

        self.add_item('enable-rotation',
                      help='Enables picture rotation',
                      fr_help="Autorise la rotation des photos",
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(pwp_type=PwpArgType.BOOL, value='true')],
                      default='true',
                      config="""

when ALBUM is moved from Synology photostation to piwigo, since piwigo assumes that pictures are not rotated,
enable-rotation should be used at least once per directory if not done when importing pictures.""",

                      fr_config="""

Dans le cas d'une transition entre Photostation (Synology) et piwigo, comme piwigo suppose que les 
photos ont été tournées correctement, il est prudent d'utiliser enable-rotation au moins une fois par dossier,
de façon à assurer que les photos sont affichées correctement.
""")

        self.add_item('enable-metadata',
                      help='Enables the generation of metadata in pictures.',
                      fr_help="Autorise la génération de métadata",
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(pwp_type=PwpArgType.BOOL, value='true')],
                      default='true',
                      config="""
CAVEAT, if true, the behavior can be modified by enable-metadata-reset and enable-date-in-filename""",
                      fr_config="""
ATTENTION: si enable-metadata est 'true', alors enable-metadata-reset et enable-date-in-filename peuvent modifier
la génération des metadata, voir aussi ces options
""")

        self.add_item('enable-conversion',
                      help='converts pictures to JPG and video to MP4.',
                      fr_help='convertis les images en JPG et les vidéos en MP4',
                      action='store',
                      setups=[ServerSetup(pwp_type=PwpArgType.BOOL, value='true')],
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      default='true',
                      config="""
CAVEAT !!!
Setting enable-conversion = false SHOULD BE AVOIDED, and used with EXTREME CARE, at your own risks.
All potential cases HAVE NOT been tested.
Keeping images/video formats not supported by piwiGo is NOT SAFE,
while conversion to JPG and MP4 is straightforward and SHOULD be preferred.  
                """,
                      fr_config="""
ATTENTION !!!
Positionner enable-conversion = false DOIT ÊTRE ÉVITÉ, et utilisé avec une EXTRÈME PRUDENCE, 
à vos risques et perils: Tous les cas potentiels n'ont PAS été testés.
Garder des formats images/vidéo qui ne sont pas supportés par piwiGo N'EST PAS SÛR,  
alors que la conversion vers JPG et MP4 est banale et DOIT être préférée.
""")

        self.add_item('enable-thumbnails',
                      help='Enables generation of Piwigo thumbnails',
                      fr_help='Autorise la génération des miniatures pour piwigo',
                      action='store',
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.FORCED,
                                          pwp_type=PwpArgType.BOOL, value='false'),
                              ServerSetup(pwp_type=PwpArgType.BOOL), ],
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      default='true')

        self.add_item('enable-remote-thumbnails',
                      help='Enables the copy of piwigo thumbnails with ssh/sftp.',
                      fr_help='Autorise la copie des miniatures pour piwigo vers le serveur piwigo, avec ssh/sftp',
                      action='store',
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.FORCED,
                                          pwp_type=PwpArgType.BOOL, value='false'),
                              ServerSetup(thumbnails=CVS.REMOTE, how=ConstraintHow.FORCED,
                                          pwp_type=PwpArgType.BOOL, value='true'),
                              ServerSetup(pwp_type=PwpArgType.BOOL), ],
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      default='false')

        self.add_item('enable-remote-album',
                      help='Enables the copy of piwigo pictures/video with ssh/sftp.',
                      fr_help='Autorise la copie des photos/vidéos vers le serveur piwigo, avec ssh/sftp',
                      action='store',
                      setups=[ServerSetup(album=CVS.UNUSED, how=ConstraintHow.FORCED,
                                          pwp_type=PwpArgType.BOOL, value='false'),
                              ServerSetup(album=CVS.REMOTE, how=ConstraintHow.FORCED,
                                          pwp_type=PwpArgType.BOOL, value='true'),
                              ServerSetup(pwp_type=PwpArgType.BOOL), ],
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      default='false')

        self.add_item('enable-remote-auto-config',
                      help='Enables the copy of auto-config .ini with ssh/sftp.',
                      fr_help='Autorise la copie des auto-config .ini le serveur piwigo, avec ssh/sftp',
                      action='store',
                      setups=[ServerSetup(album=CVS.UNUSED, how=ConstraintHow.FORCED,
                                          pwp_type=PwpArgType.BOOL, value='false'),
                              ServerSetup(album=CVS.REMOTE, how=ConstraintHow.FORCED,
                                          pwp_type=PwpArgType.BOOL, value='true'),
                              ServerSetup(pwp_type=PwpArgType.BOOL), ],
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      default='false')

        self.add_item('enable-database',
                      help='Enables the management of piwigo database information.',
                      fr_help='Autorise la gestion des informations de la base de données piwigo',
                      action='store',
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.VALUE, value="false"),
                              ServerSetup(pwp_type=PwpArgType.BOOL), ],
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      default='false')

        self.add_item('enable-auto-configuration',
                      help='Enables configuration of ALBUM from TRIAGE,' 
                           ' by creating a configuration file in AUTO-CONFIG.',
                      fr_help='Autorise la configuration automatique de ALBUM '
                              'en créant des fichiers de configuration dans AUTO-CONFIG ',
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.FORCED, value="false"),
                              ServerSetup(pwp_type=PwpArgType.BOOL), ],
                      default='true',
                      config="""
Enables the copy of piwiPre.ini files found in TRIAGE directory to the corresponding folder of AUTO-CONFIG,
so that further processing of ALBUM give the same results.""",
                      fr_config="""
Autorise la copie des fichiers piwiPre.ini trouvés dans les sous-dossiers de TRIAGE, vers le dossier
correspondant dans AUTO-CONFIG, de façon à ce que les futures vérifications de ALBUM donnent le même résultat.  
""")

        self.add_item('enable-date-in-filename',
                      help="if enable-metadata is true, reads the picture date in the filename (vs in the metadata)",
                      fr_help="si enable-metadata est 'true', lit la date des photos dans le nom de fichier"
                              " plutôt que dans les metadata",
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(pwp_type=PwpArgType.BOOL), ],
                      default='true',
                      config="""
CAVEAT: This flag should be set to false WITH CARE!

If there is a date in the filename, (according to the 'names' argument), then this date is used for metadata
Else, if there is a date in metadata, this one is kept
Else, the file creation time is used, and written in metadata

So, if a file is checked twice, the 2nd run does not perform any change

Use it ONLY when the metadata is known to be wrong, and the filename has been manually set.
It is a good practice to store it in the auto-config piwiPre.ini file
""",
                      fr_config="""
ATTENTION! Cette option doit être utilisée AVEC PRECAUTION!

Si il ya une date dans le nom de fichier (en suivant la règle définie par l''element de configuration 'name',
alors cette date est utilisée pour les metadata.
Sinon, s'il y a une date dans les métadata, cette dernière est utilisée
Sinon, on utilise la date de création du fichier.

Ainsi, si un fichier est vérifié 2 fois, la 2e fois devrait donner la même date que la 1e.

Il est prudent de n'utiliser ce flag que pour les dossiers, où les dates sont connues pour être fausse,
et doivent donc être imposées, et d'utiliser auto-config pour propager l'information dans ALBUM. 
""")

        self.add_item('enable-metadata-reset',
                      help="if enable-metadata is true, then metadata can be overwritten",
                      fr_help="si enable-metadata est 'true', alors les metadata peuvent être écrasées",
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(pwp_type=PwpArgType.BOOL), ],
                      default='false',
                      config="""
This flag is used only when enable-metadata is true.

- value = false (the default): metadata is written in the file ONLY if there was no metadata
- value = true: metadata is written if different from what was already in the file 
  (which includes no value)""",
                      fr_config="""
Cette option est utile uniquement lorsque enable-metadata est 'true'.

- valeur = false (le défaut): les metadata sont écrites dans le fichier UNIQUEMENT s'il n'y en avait pas
- valeur = true: les metadata sont écrites si différentes de ce qu'il y avait déjà dans le fichier
  (ce qui inclus le cas 'pas de valeur') 
""")

        self.add_item('enable-pwg-representative',
                      help="enables the creation of piwigo JPG representative of video",
                      fr_help="autorise la creation de l'image JPEG qui représente une vidéo dans piwigo",
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.FORCED, value="false"),
                              ServerSetup(pwp_type=PwpArgType.BOOL), ],
                      default='true')

        self.add_item('ffmpeg-path',
                      help="path to ffmpeg executable, should end with a / if not empty",
                      fr_help="chemin de du programme ffmpeg, doit finir par / si non vide",
                      action='store',
                      pwp_type=PwpArgType.DIR,
                      setups=[ServerSetup(pwp_type=PwpArgType.DIR, )],
                      default=ACTOR.linux_path(os.path.abspath((ACTOR.get_environ('PROGRAMFILES(X86)') + # noqa
                                                                '/ffmpeg/bin/'))
                                              if platform.system() == "Windows" else '/usr/bin/'),
                      config="""
- ffmpeg and ffprobe are used to handle video files.
- The default path should be OK for your system (windows or linux)
- If ffmpeg and ffprobe are in the PATH, you can leave ffmpeg-path empty
- If pwpInstaller as been used, then ffmpeg and ffprobe ARE in the path
""",
                      fr_config="""
- ffmpeg et ffprobe sont utilisés pour gérer la vidéo
- le chemin par défaut devrait être correct pour votre système (windows ou linux)
- si ffmpeg et ffprobe sont dans le PATH, ffmpeg-path peut être laissé vide
- si pwpConfigurator a été utilisé, alors ffmpeg et ffprobe SONT dans le path.                      
""")
        self.add_item('git-path',
                      help="path to git executable on WINDOWS, for INTERNAL use only",
                      fr_help="chemin vers l'exécutable git sous windows, pour usage interne seulement",
                      action='store',
                      pwp_type=PwpArgType.DIR,
                      setups=[ServerSetup(pwp_type=PwpArgType.DIR, )],
                      default='',
                      config="""
This flag is used internally ONLY with --install-exe, because piwiPre is called in the administrator context
Under normal circumstances, you should NOT use it 
""",
                      fr_config="""
Cette option est utilisée  dans un context d'élévation de privilèges,
Vous ne devriez pas avoir besoin de l'utiliser.
""")

        # ------------------------------------------------------------------------------------------------------------
        # piwigo host and users
        # ------------------------------------------------------------------------------------------------------------

        self.add_header("""
Management of piwigo host and users 
===================================""")

        self.add_header("""
Gestion de l'hôte piwigo et des utilisateurs 
============================================""", lang='fr')

        # --------------------------------------
        # ssh/sftp

        self.add_item('ssh-user',
                      help='username on remote server, used for ssh/sftp',
                      fr_help="nom de l'utilisateur de ssh/sftp sur le serveur distant",
                      action='store',
                      default="",
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(album=CVS.REMOTE, how=ConstraintHow.VALUE, value="username ?"),
                              ServerSetup(thumbnails=CVS.REMOTE, how=ConstraintHow.VALUE, value="username ?"),
                              ServerSetup(album=CVS.LOCAL, thumbnails=CVS.LOCAL, how=ConstraintHow.FORCED, value=''),
                              ServerSetup()],
                      config="""
- Value = 'string' :username on remote server, used by ssh/sftp
- Value = None : anonymous ssh/sftp is assumed""",
                      fr_config="""
- Valeur = 'string' : utilisateur du serveur distant, pour ssh/sftp
- Valeur = None : ssh/sftp anonyme
""")

        self.add_item('ssh-host',
                      help='sets the hostname of the piwigo server, used by ssh/sftp',
                      fr_help="indique le nom du serveur ssh/sftp distant",
                      action='store',
                      default="",
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(album=CVS.REMOTE, how=ConstraintHow.VALUE, value="hostname ?"),
                              ServerSetup(thumbnails=CVS.REMOTE, how=ConstraintHow.VALUE, value="hostname ?"),
                              ServerSetup(album=CVS.LOCAL, thumbnails=CVS.LOCAL, how=ConstraintHow.FORCED, value=''),
                              ServerSetup()],
                      config="""
- Value = 'string' : hostname of the host, used by ssh
- Value = None : remote ssh cannot be used""",
                      fr_config="""
- Valeur = 'string' : nom du serveur 
- Valeur = None : ssh/sftp impossible
""")

        self.add_item('ssh-port',
                      help='ssh/sftp port the piwigo server',
                      fr_help="port ssh du serveur distant distant",
                      action='store',
                      setups=[ServerSetup()],
                      pwp_type=PwpArgType.INT,
                      default=42)

        self.add_item('ssh-incoming',
                      help='Path, relative to the remote directory where SFTP launches, where files can be written.',
                      fr_help="Chemin, relatif au dossier dans lequel SFTP arrive, dans lequel SFTP peut écrire",
                      action='store',
                      default="",
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(album=CVS.REMOTE, how=ConstraintHow.VALUE, value="Path ?"),
                              ServerSetup(thumbnails=CVS.REMOTE, how=ConstraintHow.VALUE, value="Path ?"),
                              ServerSetup(album=CVS.LOCAL, thumbnails=CVS.LOCAL, how=ConstraintHow.FORCED, value=''),
                              ServerSetup()],
                      config="""
If None, the SFTP root should be writable.

'incoming' is a typical value""",
                      fr_config="""
- Valeur = None, le repertoire racine de SFTP doit être autorisé en écriture .
- Valeur = 'incoming' est une valeur typique""")

        # --------------------------------------
        # piwigo

        self.add_item('piwigo-user',
                      help='username for piwigo access',
                      fr_help="nom d'utilisateur piwigo pour l'accès aux photos/vidéo/dossiers",
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.VALUE, value=""),
                              ServerSetup()],
                      action='store',
                      default="")

        self.add_item('piwigo-level',
                      help='default piwigo confidentiality level for new piwigo directories',
                      fr_help="niveau de confidentialité par défaut des nouveaux dossiers piwigo",
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.VALUE, value=""),
                              ServerSetup()],
                      action='store',
                      default='0')
        # --------------------------------------
        # sql

        self.add_item('sql-user',
                      help='username sql server',
                      fr_help="nom de l'utilisateur du serveur SQL",
                      action='store',
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.VALUE, value=""),
                              ServerSetup()],
                      default="",
                      config="""
- Value = 'string' :username on sql server
- Value = None : anonymous sql access is assumed
""")

        self.add_item('sql-pwd',
                      help='Sets the password of the sql access ',
                      fr_help="mot de passe de l'utilisateur du serveur SQL",
                      action='store',
                      pwp_type=PwpArgType.PASSWORD,
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.VALUE, value=""),
                              ServerSetup(pwp_type=PwpArgType.PASSWORD, value=""),
                              ServerSetup(location='config')],
                      default="",
                      location='config')

        self.add_item('sql-host',
                      help='sets the hostname of the sql server',
                      fr_help="nom du serveur SQL",
                      action='store',
                      pwp_type=PwpArgType.STR,
                      default="",
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.VALUE, value=""),
                              ServerSetup()],
                      config="""
If None, SQL cannot be used""",
                      fr_config="""
Si None, SQL ne peut pas être utilisé""")

        self.add_item('sql-port',
                      help='sets the port for the sql server',
                      fr_help="port du serveur SQL",
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.VALUE, value=""),
                              ServerSetup()],
                      action='store',
                      pwp_type=PwpArgType.INT,
                      default=1433)

        self.add_item('sql-database',
                      help='sets the database name of the sql server',
                      fr_help="nom de la base de donnée piwigo sur le serveur SQL",
                      action='store',
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(thumbnails=CVS.UNUSED, how=ConstraintHow.VALUE, value=""),
                              ServerSetup()],
                      default="piwigo")

        # ------------------------------------------------------------------------------------------------------------
        # remote host configuration
        # ------------------------------------------------------------------------------------------------------------

        self.add_header("""
       
remote host configuration
=========================
Modify these settings only if you know exactly what you are doing.
The default values should be ok with any standard Linux remote host.""")

        self.add_header("""

configuration de l'hôte distant
===============================
Ne modifiez ces valeurs que si vous êtes **certain** de ce que vous faites.
Les valeurs par défaut sont correcte pour la plupart des serveurs Linux""", lang='fr')

        self.add_item('ls-command',
                      help='The remote shell command to list files.',
                      fr_help="La commande distante pour lister les fichiers",
                      action='store',
                      pwp_type=PwpArgType.STR,
                      default='ls -sQ1HL --full-time "{file}"',
                      # setups=[ServerSetup(pwp_type=PwpArgType.STR, how=ConstraintHow.HIDDEN)],
                      location='config')
        # -H    follow symbolic links listed on the command line
        # -s    print the allocated size of each file, in blocks
        # -Q    enclose entry names in double quotes
        # -1    list one file per line.  Avoid '\n' with -q or -b
        # -L    show information for the file the link references rather than for the link itself
        # --full-time  uses iso time format
        # examples:
        # '100 -rwxrwxrwx 1 foo root   98506 2024-01-17 13:28:54.779010748 +0100 "top.html"'        # noqa
        # '  4 drwxrwxr-x  2 fabien other  4096 2023-09-06 13:30:47.775207946 +0200 "Public"'       # noqa

        self.add_item('ls-output',
                      help='The output of ls-command.',
                      fr_help="Le format de sortie de ls-command",
                      action='store',
                      pwp_type=PwpArgType.STR,
                      default=r' *\d+ +{flags} +\d+ +\w+ +\w+ +' +
                              r'{size}\s+{Y}-{m}-{d} {H}:{M}:{S}\.{ms} {z}\s+"{file}"',
                      # setups=[ServerSetup(pwp_type=PwpArgType.STR, how=ConstraintHow.HIDDEN)],
                      location='config',
                      config=r"""
Where flags are taken from 
https://docs.python.org/3/library/datetime.html?highlight=datetime#strftime-strptime-behavior ,

- {dir} is 'd' for a directory
- {size} is the file size in K Bytes
- {file} is the file name
- {Y} is the year, with 4 digits
- {m} is the month number, with 2 digits
- {d} is the day number with 2 digits
- {H} is the hour, with 2 digits
- {M} the minutes, with 2 digits
- {S} the seconds, with 2 digits
- {ms} the milliseconds
- {z} the timezone, expressed as the number of hours and minutes of difference with UTC time, 
  eg. +0100 for CET during winter.
- {am} is AM or PM
- {flags} is the file mode 

Alternative for ms-dos, see https://www.windows-commandline.com/get-file-modified-date-time/

- 'dir {file}'
- '{Y}/{m}/{d} {H}:{M} {am}'\d*\s+{file}'""",
                      fr_config=r"""
Les valeurs sont similaires à: 
https://docs.python.org/3/library/datetime.html?highlight=datetime#strftime-strptime-behavior ,

- {dir} est l'indicateur 'd' de dossier 
- {size} est la taille du fichier en K Octets
- {file} est le nom de fichier
- {Y} est l'année, sur 4 chiffres
- {m} est le numéro de mois, sur 2 chiffres
- {d} est le numéro de jour sur 2 chiffres
- {H} est l'heure, sur 2 chiffres
- {M} est la minute, sur 2 chiffres
- {S} est la seconde, sur 2 chiffres
- {ms} est la milliseconde
- {z} est le fuseau horaire, exprimé comme la difference en heures/minutes par rapport au temps UTC 
  eg. +0100 pour CET en hiver.
- {am} est AM oo PM
- {flags} est le 'mode' du fichier 

Alternative pour ms-dos, voir https://www.windows-commandline.com/get-file-modified-date-time/

- 'dir {file}'
- '{Y}/{m}/{d} {H}:{M} {am}'\d*\s+{file}'""")

        # -------------------------------------------------------------------
        # cmdline only
        # -------------------------------------------------------------------

        self.add_header("""
cmdLine flags only
==================

The following command line arguments do not have configuration counterpart in the .ini file:
""")

        self.add_header("""
Les options de configuration spécifiques de la ligne de commande
=================================================================

Les options suivantes n'ont pas de contrepartie dans les fichiers .ini, 
et ne peuvent donc être utilisés que sur la ligne de commande
""",
                        lang='fr')

        # -h, --help is implicit
        self.add_item('quiet',
                      action='store',
                      help="Does not print the initial banner with log information.",
                      fr_help="N'imprime pas la bannière initiale",
                      location='args',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(how=ConstraintHow.CMDLINE, value='false', pwp_type=PwpArgType.BOOL, )],
                      default='false'
                      )

        self.add_item('gui',
                      help="Display the graphical user interface.",
                      fr_help="Affiche l'interface graphique",
                      location='args',
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(how=ConstraintHow.HIDDEN, value='false', pwp_type=PwpArgType.BOOL,
                                          location='arg')],
                      default='false')

        self.add_item('home',
                      help="Change the location of HOME, so a different .piwiPre.ini is read (handled after --base)",
                      fr_help="Change HOME, ainsi un different .piwiPre.ini est lu (géré après --base)",
                      location='args',
                      action='store',
                      pwp_type=PwpArgType.DIR,
                      setups=None,  # We do NOT want this to appear in the UI, too dangerous
                      default=os.path.expanduser("~"),
                      config="""
This is something you do NOT do in normal situation, only for test
                      """,
                      fr_config="""
Cette option n'est en principe utilisée que dans le cas du test
"""
                      )

        self.add_item('version',
                      action='store_true',
                      help="Prints piwiPre version number and exits.",
                      fr_help="Imprime la version de piwiPre et sort",
                      location='args',
                      pwp_type=PwpArgType.PRESENT,
                      config="""
This flag has no value, it is active only when set
Usually used with --quiet
""",
                      fr_config="""
Cette option  n'a aucune valeur, elle n'est active que si utilisée.
Utilisé habituellement avec --quiet
""")
        self.add_item('full-help',
                      action='store_true',
                      help="Prints piwiPre extended help and exits.",
                      fr_help="Imprime l'aide étendue de piwiPre et sort",
                      location='args',
                      pwp_type=PwpArgType.PRESENT,
                      config="""
This flag has no value, it is active only when set""",
                      fr_config="""
Cette option  n'a aucune valeur, elle n'est active que si utilisée.
                """)

        self.add_item('licence',
                      action='store_true',
                      help="prints the LICENCE and exits",
                      fr_help="imprime la LICENCE et sort",
                      location='args',
                      pwp_type=PwpArgType.PRESENT,
                      config="""
This flag has no value, it is active only when set""",
                      fr_config="""
Cette option  n'a aucune valeur, elle n'est active que si utilisée.
""")

        self.add_item('debug',
                      help="Increments the level of verbosity of the logs printed on standard output.",
                      fr_help="Incrémente le niveau de verbosité des logs affichés sur la sortie standard.",
                      location='args',
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(how=ConstraintHow.CMDLINE, value='false', pwp_type=PwpArgType.BOOL,
                                          location="arg")],
                      default='false',
                      )

        self.add_item('stop-on-warning',
                      help="Stops piwiPre at the first warning.",
                      fr_help="Stoppe piwiPre au premier avertissement (Warning)",
                      location='args',
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(how=ConstraintHow.CMDLINE, value='false', pwp_type=PwpArgType.BOOL,
                                          location="arg", )],
                      default='false', )

        self.add_item('trace-malloc',
                      action='store_true',
                      help="Uses trace-malloc to look for memory leaks, use at your own risks...",
                      fr_help="Utilise trace-malloc pour rechercher des memory-leaks, reservé aux développeurs",
                      location='args',
                      pwp_type=PwpArgType.PRESENT,
                      config="""
This flag has no value, it is active only when set""",
                      fr_config="""
Cette option  n'a aucune valeur, elle n'est active que si utilisée.
        """)

        self.add_item('dump-config',
                      pwp_type=PwpArgType.DIR,
                      action='store',
                      help="Dump the configuration for a given directory and exits.",
                      fr_help="Affiche la configuration pour le repertoire argument, et sort",
                      location='args',
                      setups=[ServerSetup(how=ConstraintHow.CMDLINE, value='', pwp_type=PwpArgType.DIR,
                                          location="arg", )],
                      config="""
The value of this flag is the name of the directory from which the configuration should be dumped.

This path starts from BASE, e.g. TRIAGE/Armor""",
                      fr_config="""
La valeur de cette option est le nom du repertoire dont on veut afficher la configuration.

Le chemin part depuis BASE, par exemple TRIAGE/Armor""")

        self.add_item('dryrun',
                      help="Prints what should be done, but does not execute actions.",
                      fr_help="Affiche les actions que piwiPre devrait faire, mais ne les réalise pas",
                      location='args',
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(how=ConstraintHow.CMDLINE, value='false', pwp_type=PwpArgType.BOOL,
                                          location="arg", )],
                      default='false',
                      config="""
CAVEAT:

    dryrun tries to display all potential actions that would be made, 
    but there are some limitations. 
    For instance, dryrun does NOT correctly detect all thumbnail-related activities.
                              """,
                      fr_config="""

ATTENTION:
    dryrun essaie d'afficher toutes les actions potentielles qui pourraient être réalisées,
    mais il y a des limitations à ce qu'il peut découvrir.
    En particulier, dryrun n'affiche pas correctement l'intégralité des actions relatives au miniatures (thumbnails)
""")

        self.add_item('base',
                      help="Changes BASE, the directory where piwiPre is run, is always executed BEFORE --home",
                      fr_help="Change BASE, le dossier d'où est exécuté piwiPré, toujours effectué AVANT --home",
                      pwp_type=PwpArgType.DIR,
                      setups=None,  # We do NOT want this to appear in the UI, too dangerous
                      default=os.getcwd(),
                      action='store',
                      location='args')
        # CAVEAT: base in NEVER in the config file
        # and if we have --base as an argument, piwipre will do an os.chdir() to change cwd

        self.add_item("enable-create-base",
                      help="allows piwiPre to create BASE (and TRIAGE) if not existing",
                      fr_help="Autorise piwiPre à créer BASE (et TRIAGE) s'il n'existe pas",
                      pwp_type=PwpArgType.BOOL,
                      action='store',
                      location='args',
                      setups=None,  # We do NOT want this to appear in the UI, too dangerous
                      default=False,
                      config="This is seldom used, excepted when piwiPre is started by pwpInstaller",
                      fr_config="Utilisé uniquement en cas de lancement par pwpInstaller")

        self.add_item('base-last',
                      help="like --base, but changes to the LAST directory where piwiPre was run,",
                      fr_help="Comme --base, mais vers le DERNIER dossier d'où piwiPré a été lancé,",
                      pwp_type=PwpArgType.BOOL,
                      choices=['true', 'false'],
                      location='args',
                      setups=None,  # We do NOT want this to appear in the UI, too dangerous
                      default='false',
                      action='store')

        self.add_item('enable-verify-sub-album',
                      help="Makes --verify-album recursive (go in sub-directories)",
                      fr_help="Rend --verify-album récursif (va dans les sous-dossiers)",
                      action='store',
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      setups=[ServerSetup(pwp_type=PwpArgType.BOOL,
                                          location="args", )],
                      default='false',
                      location='args')

        self.add_item('restart-from-dir',
                      help="During verify-album, restart from this directory",
                      fr_help='Pendant verify-album, repart de ce sous-repertoire',
                      pwp_type=PwpArgType.DIR,
                      action='store',
                      location='args',
                      setups=None,  # We do NOT want this to appear in the UI, too dangerous
                      config="""
Directories to verify are  sorted in alphanumerical order.

Directories less than the argument are not managed.

The argument is the first managed.

If the argument is does not start with the value of --verify-album, then restart-from-dir is ignored,
because there is no chance that this would be a sub-directory.  

If the argument starts with the same value than the value of --verify-album, but the directory is not found,
then an error is raised.


For instance, next line will start verifying at 2012/2012-08-Aout-03-Example

    piwiPre --verify-album 2012 --restart-from-dir 2012/2012-08-Aout-03-Example

but next line will verify 2013

    piwiPre --verify-album 2013 --restart-from-dir 2012/2012-08-Aout-03-Example

and next line will generate an error if 2012/wrong-subdir does not exist 

    piwiPre --verify-album 2012 --restart-from-dir 2012/wrong-subdir

This flag may be useful to restart processing that was interrupted
    """,
                      fr_config="""
Les dossiers à vérifier sont triés dans l'ordre lexicographique.

Les dossiers 'avant' l'argument ne sont pas vérifiés.

Le dossier argument est le premier trié.

Si l'argument de --restart-from-dir ne commence pas par la valeur de --verify-album, sa valeur est ignorée, puisque ce ne peut pas
être un sous-dossier de ALBUM.

Si l'argument de --restart-from-dir n'est pas trouvé dans l'album, alors une erreur est générée.

Par exemple, la ligne suivante démarre la vérification à 2012/2012-08-Aout-03-Example:

    piwiPre --verify-album 2012 --restart-from-dir 2012/2012-08-Aout-03-Example

Mais la ligne suivante vérifie 2013 entièrement:

    piwiPre --verify-album 2013 --restart-from-dir 2012/2012-08-Aout-03-Example

et la ligne suivante génère une erreur si 2012/wrong-subdir n'existe pas  

    piwiPre --verify-album 2012 --restart-from-dir 2012/wrong-subdir

""")  # noqa

        # --------------------------------------------------------------
        # self test

        self.add_header("""
.. attention::
    The following flags --test-xxx are used when performing self-testing of piwiPre
    They are not intended to be used under normal circumstances""")

        self.add_header("""
.. attention::
    Les options suivantes, de la forme --test-XXX sont utilisés lors de l'autotest de piwiPre,
    et ne sont donc pas sensés être utilisés dans des circonstances habituelles        
""",
                        lang='fr')

        self.add_item('test-ssh',
                      help="tests ssh on remote host and exits",
                      fr_help="teste la communication ssh avec l'hôte distant et sort",
                      action='store_true',
                      pwp_type=PwpArgType.PRESENT,
                      setups=[ServerSetup(pwp_type=PwpArgType.STR,
                                          location="args",
                                          how=ConstraintHow.CMDLINE)],
                      location='args')

        self.add_item('test-sftp',
                      help="tests sftp on remote host (by copying a file in HOME) and exit",
                      fr_help="teste sftp avec l'hôte distant (en copiant un fichier dans HOME) et sort",
                      action='store_true',
                      pwp_type=PwpArgType.PRESENT,
                      setups=[ServerSetup(pwp_type=PwpArgType.STR,
                                          location="args",
                                          how=ConstraintHow.CMDLINE)],
                      location='args')

        self.add_item('test-sql',
                      help="tests SQL access on sql host by looking at first picture",
                      fr_help="teste l'accès SQL avec le serveur en atteignant la 1ere image",
                      action='store_true',
                      pwp_type=PwpArgType.PRESENT,
                      setups=[ServerSetup(pwp_type=PwpArgType.STR,
                                          location="args",
                                          how=ConstraintHow.CMDLINE)],
                      location='args')

        self.add_item('test-gui-dismiss-errors',
                      help="For tests of the the graphical interface",
                      fr_help="Pour les tests de l'interface graphique",
                      action='store',
                      choices=['true', 'false'],
                      default='false',
                      pwp_type=PwpArgType.BOOL,
                      location='args')

        # -------------------------------------------------------------------
        # configuration globale
        # -------------------------------------------------------------------

        self.add_header("""
Global configuration 
====================

The following configuration items are global, and accessible through command line options
and configuration file.""")

        self.add_header("""
Configuration globale
=====================

Les options globales de configuration, sont accessibles dans un fichier de configuration
ou sur la ligne de commande        
        """,
                        lang='fr')
        self.add_item('names',
                      help='The format of renamed pictures/video. This includes the path starting from ALBUM.',
                      fr_help="Le format des nouveaux nom d'images/video. Inclus le chemin depuis la racine de ALBUM",
                      action='store',
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup()],
                      default='{Y}/{Y}-{m}-{month_name}-{d}-{radical}/{Y}-{m}-{d}-{H}h{M}-{S}-{radical}.{suffix}',
                      location='both',
                      config=r"""

CAVEAT: The value must be enclosed in single or double quotes !                      
                      
Field values:

- {Y} etc are inherited from the IPTC date of the picture.

- {radical} is the name of the TRIAGE folder where the picture was originally found.

- {author} is computed according to the camera name in the IPTC metadata, see **authors**

- {count} is the current count of pictures in the directory,
  so that it is 01 for the first picture, 02 for the 2nd etc.

- {suffix}: file suffix, typically jpg, txt, mp4...

- All numeric fields are printed with 2 digits, excepted year which has 4.

When several  different pictures are supposed to have the same filename,
the last numeric field (here {s}) is incremented until a unique filename is found.


Many users prefer names that include the date,
so that name collisions are avoided when pictures are out in a flat folder.

But different schemes are possible.
For instance, "{Y}/{m}/{d}/{radical}-{count}", is also a traditional naming.

all characters that are not in 
"a-zA-Z0-9\-_.&@~!,;+°()àâäéèêëïîôöùûüÿçñÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÇÑ " will be replaced by '_' 
""",  # noqa
                      fr_config="""
ATTENTION: la valeur doit être insérées entre des apostrophes simples ou doubles ' ou "

La valeur des champs:

- {Y} etc sont hérités de la date de prise de vue dans les données IPTC de l'image

- {radical} est le nom du dossier de TRIAGE dans lequel le fichier a été trouvé.

- {author} est calculé en fonction des données IPTC, voir **authors** 

- {count} est le numéro courant de fichier dans le dossier, 
  c'est à dire 01 pour le 1er fichier, 02 pour le suivant etc...

- {suffix}: l'extention du nom de fichier: jpg, txt, mp4...

- toutes les données numériques sont affichées avec 2 chiffres, sauf l'année qui est sur 4
 
""")  # noqa

        self.add_item('month-name',
                      help='The name for each month, used to rename files.',
                      fr_help='Le nom de chaque mois, utilisé renommer les fichiers.',
                      action='store',
                      pwp_type=PwpArgType.LIST,
                      default=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                      fr_default=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet',  # noqa
                                  'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
                      # setups=[ServerSetup(pwp_type=PwpArgType.LIST, how=ConstraintHow.HIDDEN)],
                      setups=None,  # we DO NOT want to see month-name in the UI, until with have a multiline UI
                      location='config')

        self.add_item('copyright',
                      help='A copyright sentence to be written in Exif metadata, with obvious fields.',
                      fr_help="Une phrase de Copyright à écrire dans les données EXIF, dont les champs sont évidents",
                      action='store',
                      default="(C) {author} {Y}",
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(pwp_type=PwpArgType.STR,
                                          location="both", )],
                      location='both',
                      config="""- The date is taken from the photo metadata, {month} and {day} are also available.'""",
                      fr_config="""
        - La date est prise dans les meta-données de la photo, {month} et {day} sont disponibles
        """)

        self.add_item('instructions',
                      help="A sentence to be written in Exif metadata, with {author} coming from the 'authors' section",
                      fr_help="Une phrase à écrire dans les meta-données EXIF, avec {author} qui provient de la "
                              "section 'auteurs'",
                      action='store',
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(pwp_type=PwpArgType.STR,
                                          location="both")],
                      default="No copy allowed unless explicitly approved by {author}",
                      fr_default="Aucune copie autorisée sauf si explicitement approuvée par {author}",
                      location='both',
                      config="""- adding an email or a phone number may be appropriate.""",
                      fr_config="""- il peut être intéressant de rajouter un email, un numéro de téléphone...""")

        self.add_item('authors',
                      help='A dictionary of mappings between camera model name as found in Exif data, and author name',
                      fr_help="Un dictionnaire qui fait le lien entre le nom de l'appareil photo dans les données EXIF,"
                              "et les auteurs",
                      action='store',
                      pwp_type=PwpArgType.DICT,
                      # setups=[ServerSetup(pwp_type=PwpArgType.DICT, how=ConstraintHow.HIDDEN)],
                      setups=None,  # we DO NOT want to see authors in the UI, until with have a multiline UI
                      default={},
                      location='config',
                      config="""
- example of possible value ::

   Camera1 : author1
   'Camera 2' : 'author 2'
   DEFAULT : 'default value'

""",
                      fr_config="""
- example de valeurs ::

   Camera1 : author1
   'Camera 2' : 'author 2'
   DEFAULT : 'default value'
   
""")
        # -------------------------------------------------------------------
        # configuration only
        # -------------------------------------------------------------------

        self.add_header("""
configuration only
==================

The following configuration items are not accessible through command line options
and must be specified in a configuration file.""")

        self.add_header("""
configuration seulement
=======================

Les options suivantes, sont complexes, et ne sont utilisées que dans un fichier de configuration        
    """,
                        lang='fr')

        self.add_item('dates',
                      help='A dictionary of dates corrections',
                      fr_help="Un dictionnaire de correction de dates",
                      action='store',
                      pwp_type=PwpArgType.DICT,
                      default='',  # {},
                      # setups=[ServerSetup(pwp_type=PwpArgType.DICT, how=ConstraintHow.HIDDEN)],
                      setups=None,
                      location='config',
                      config="""
Date corrections are used only to compute the new name of the picture in the renaming step.
The metadata (notably dates) of the picture is unchanged.

- indents are 4 character wide and are significant
- each toplevel item a dictionary with a unique name
- each date is written as a dictionary with year, month, day, hour, minute, second, some items may be missing

- the correction is described by a dictionary with the following fields:

  - 'start', 'end': dates. the correction occurs if the picture date is between these boundaries
  - camera_name: the name of the camera for this correction or 'default' for camera name not in the list
  - 'delta' or 'forced' : a date. 
  
    - If 'delta', the date is added to the picture date, the items are increments, the names use plural form:
      years, months, days, hours, minutes, seconds 
    - If  'forced' the picture date is set to this value.

- the specific 'NO-DATE' toplevel item is for pictures without a date in metadata.
   - the 'start', 'end', delta dates are not defined
   - this item contains only 'forced' date that will be set to all pictures without a date
   - Si hour, minute, second are not specified, piwiPre uses the picture creation time.
   
See also the online documentation 
   """,
                      fr_config="""

La correction de date est utilisée pour calculer le nouveau nom du fichier.                      
Les metadata du fichier, en particulier la date, ne sont PAS modifiés.

- Les indentations, de 4 caractères, représentent le 'niveau' d'un objet, et sont donc significatives
- Chaque élément de 1er niveau a un nom unique et renvoie vers un dictionnaire
- Chaque date est écrite sout forme d'un dictionnaire year, month, day, hour, minute, second, dont certains éléments
  peuvent être omis
  
- Une modification est décrite par un dictionnaire avec les champs suivants:

  - 'start', 'end': des dates. La correction est effectuée sir la date de la photo est comprise entre ces 2 bornes
  - camera_name: le nom de la camera, ou bien 'default' pour toutes les caméras qui ne sont pas listées
  - 'delta' ou 'forced': une date.
  
    - si 'delta': la date est AJOUTÉE à la date courante. donc les valeurs de la date sont des incréments, 
      possiblement négatifs, dont le nom est au pluriel: years, months, days, hours, minutes, seconds
      
    - si 'forced', la date de le photo est mise à cette valeur

- l'élément de 1er niveau 'NO-DATE' est pour les photos qui n'ont pas de date dans les metadata
     
   - 'start' et 'end' ne sont pas définis
   - cette modification contient uniquement un item 'forced', qui indique la nouvelle date des photos sans date
   - si hour, minute, second ne sont pas définis dans 'forced', alors ce sont les valeurs de la date de création 
     du fichier qui sont pris
     
- Voir aussi la documentation en ligne       
""")

        self.add_header("""
example ::

    dates:
        USA:                 # this name should be unique within the 'dates'
            start:
                year:  2018
                month:  7
                day: 4
                hour: 20
            end:
                year:  2018
                month:  7
                day: 6
                hour: 23
            D6503:              # camera name
                delta:
                    hour: 9
            TG-320:            # a different camera
                delta:
                    hour: 9
                    minute: 30
        Utah 1:
            start:
                year:  2018
                month:  7
                day: 6
                hour: 23
            end:
                year:  2018
                month:  7
                day: 8
                hour: 23
            TG-320 :
                delta:
                    hours: 8   # CAVEAT: here, hours and not hour ! (and years, etc...)
        NO-DATE:               # CAVEAT: like python, yaml is strict on indentation errors
            forced :
                 year: 2023
                 month: 7
                 day : 24

.. Note:: usually, 'NO-DATE' and  'forced' are not set on a global ALBUM basis, 
   but rather in a specific TRIAGE or ALBUM folder where abnormal pictures are known to be stored.
   

.. Important:: unless enable-auto-configuration == false,  
   when a .ini file is stored in a TRIAGE folder or sub-folder, 
   then it  will be copied in the corresponding AUTO-CONFIG subdirectories,  
   so that further processing of ALBUM give the same results. 
   This is particularly useful for dates management
""")
        self.add_header("""
exemple ::

    dates:
        USA:                 # Ce nom de modification doit être unique dans tout le dictionnaire
            start:
                year:  2018
                month:  7
                day: 4
                hour: 20
            end:
                year:  2018
                month:  7
                day: 6
                hour: 23
            D6503:              # nom de l'appareil photo
                delta:
                    hour: 9
            TG-320:            # un autre appareil photo
                delta:
                    hour: 9
                    minute: 30
        Utah 1:
            start:
                year:  2018
                month:  7
                day: 6
                hour: 23
            end:
                year:  2018
                month:  7
                day: 8
                hour: 23
            TG-320 :
                delta:
                    hours: 8   # ATTENTION: ici, hours et non pas hour ! (et years, etc...)
        NO-DATE:               # ATTENTION: respecter les indentations de 4 caractère
            forced :
                 year: 2023
                 month: 7
                 day : 24

.. Note:: habituellement, 'NO-DATE' and  'forced' ne sont pas positionnés pour l"intégralité d'un album, 
   mais plutot dans 1 repertoire spé&cifique de TRIAGE puis d'ALBUM, dans lequel on sait que les metadata sont fausses.
   

.. Important:: Sauf si  enable-auto-configuration == false, 
   quand un .ini existe dans un (sous) dossier de TRIAGE,
   alors il sera recopié dans le sous-repertoire correspondant de THUMBNAILS,
   de façon à ce que la gestion suivante de ALBUM donne les mêmes resultats.
   C'est particulièrement utile pour la gestion des dates.

""", 'fr')  # noqa

        self.add_item('piwigo-thumbnails',
                      help="A dictionary of piwigo thumbnails to be built, including formats",
                      fr_help="Un dictionnaire des miniatures pour piwigo, incluant les formats",
                      action='store',
                      pwp_type=PwpArgType.DICT,
                      default={
                          "{f}-sq.jpg": {'width': 120, 'height': 120, 'crop': True},
                          "{f}-th.jpg": {'width': 144, 'height': 144, 'crop': False},
                          "{f}-me.jpg": {'width': 792, 'height': 594, 'crop': False},
                          "{f}-cu_e250.jpg": {'width': 250, 'height': 250, 'crop': True},
                      },
                      # setups=[ServerSetup(pwp_type=PwpArgType.DICT, how=ConstraintHow.HIDDEN)],
                      setups=None,
                      location='config',
                      config="""
A dictionary if thumbnail specifications,

- {f} is the photo basename
- width = maximum width
- height = maximum height
- crop = the picture will be cropped to a square form factor.

The regular piwigo thumbnails defined in the documentation are as follows ::

    "{f}-sq.jpg" : 120, 120, crop      # SQUARE: mandatory format
    "{f}-th.jpg":  144, 144            # THUMB:  mandatory
    "{f}-me.jpg" : 792, 594            # MEDIUM: mandatory
    "{f}-2s.jpg" : 240, 240            # XXSMALL       # noqa
    "{f}-xs.jpg" : 432, 324            # XSMALL        # noqa
    "{f}-sm.jpg" : 576, 432            # SMALL
    "{f}-la.jpg" : 1008, 756           # LARGE
    "{f}-xl.jpg" : 1224, 918           # XLARGE        # noqa
    "{f}-xx.jpg" : 1656, 1242          # XXLARGE       # noqa
    "{f}-cu_e250.jpg" : 250, 250, crop # CU    : mandatory""", # noqa
                      fr_config="""
Un dictionnaire des specifications des miniatures:

- {f} est le nom du fichier, sans l'extension
- width = largeur maximale
- height = hauteur maximale
- crop = l'image sera découpée en format carré

La liste des miniatures piwigo telle que trouvée dans la documentation ::

    "{f}-sq.jpg" : 120, 120, crop      # SQUARE: obligatoire 
    "{f}-th.jpg":  144, 144            # THUMB:  obligatoire
    "{f}-me.jpg" : 792, 594            # MEDIUM: obligatoire
    "{f}-2s.jpg" : 240, 240            # XXSMALL       # noqa
    "{f}-xs.jpg" : 432, 324            # XSMALL        # noqa
    "{f}-sm.jpg" : 576, 432            # SMALL
    "{f}-la.jpg" : 1008, 756           # LARGE
    "{f}-xl.jpg" : 1224, 918           # XLARGE        # noqa
    "{f}-xx.jpg" : 1656, 1242          # XXLARGE       # noqa
    "{f}-cu_e250.jpg" : 250, 250, crop # CU    : obligatoire                     
                      """),  # noqa

        self.add_header("""
Language management and Misc
============================
"""),

        self.add_header("""
Gestion de la langue et divers
==============================
""", 'fr'),

        self.add_item('language',
                      help="sets the language for help and a few options",
                      fr_help="change la langue pour l'aide et quelques options",
                      action='store',
                      pwp_type=PwpArgType.STR,
                      setups=[ServerSetup(pwp_type=PwpArgType.STR, )],
                      choices=['en', 'fr'],
                      default="en",
                      fr_default='fr',
                      config="""
Changing the language as an effect on the **default** values of **names**, **month-name**, **copyright**
and  **--help** prints the help in the chosen language
""",
                      fr_config="""
Changer la langue a un effet sur les valeurs **par défaut** des options suivantes: **names**, **month-name**, 
**copyright** et  **--help** imprime l'aide dans la langue choisie.

Le nom des options n'est PAS traduit, par exemple --help reste --help, ne devient pas --aide
""")
        self.add_item('enable-colors',
                      help="Prints output with colors",
                      fr_help="Imprime sur le terminal avec des couleurs",
                      action='store',
                      setups=[ServerSetup(pwp_type=PwpArgType.BOOL)],
                      choices=['true', 'false'],
                      pwp_type=PwpArgType.BOOL,
                      default='true')

        self.config = self.parse_args_and_ini(program,
                                              self.default_ini_file,
                                              arguments,
                                              with_config=with_config) if parse_args else None


def build_official_rst(autotest: bool):
    if autotest:
        filename_en = "tests/results/configuration.rst"
        filename_fr = "tests/results/configuration_fr.rst"
    else:
        filename_en = 'source/usage/configuration.rst'
        filename_fr = 'source/fr/configuration.rst'

    source = 'piwiPre/pwpParser.py'
    if not autotest and os.path.getmtime(filename_en) > os.path.getmtime(source):
        LOGGER.msg(f"file '{filename_en}' is older than source '{source}': patch useless")
        return
    parser = PwpParser(arguments=[], with_config=True, program="autotest")
    LOGGER.msg(f"building english rst '{filename_en}' from '{source}'")
    parser.build_rst(filename_en, lang='en')
    LOGGER.msg(f"construction du rst français '{filename_en}' depuis '{source}'")
    parser.build_rst(filename_fr, lang='fr')


def pwp_parser_main(arguments):
    LOGGER.msg('--------------- starting pwp_test_config')
    parser = PwpParser(arguments=arguments, program="parser_autotest", with_config=False)
    config = parser.parse_args_and_ini("test harness", "test.ini", arguments)
    rst = "../results/test-result.rst"
    ini = "../results/test-result.ini"
    parser.build_rst(rst)
    parser.write_ini_file(ini)
    pprint.pprint(config)
    parser.print_help()
    LOGGER.msg('--------------- end of  pwp_test_config')


if __name__ == "__main__":
    sys.exit(pwp_parser_main(sys.argv[1:]))
