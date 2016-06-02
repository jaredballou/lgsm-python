#!/usr/bin/python
import argparse
import os
import subprocess
import tarfile
import zipfile


def extract_file(compressed_file, target_path):
  """
  extract_file(compressed_file, target_path)

  extracts the compressed_file to target_path
  """

  if os.path.exists(compressed_file):
    print "Extracting %s to %s\n" % (compressed_file, target_path)

    if zipfile.is_zipfile(compressed_file):
      with zipfile.ZipFile(compressed_file, "r") as z:
          z.extractall(path=target_path)

    if tarfile.is_tarfile(compressed_file):
      tar = tarfile.open(compressed_file)
      tar.extractall(path=target_path)
      tar.close()

    print "Cleaning up\n"
    os.remove(compressed_file)

    print "Done!\n"
  else:
    print "%s does not exist, cannot extract" % compressed_file


def get_url(plugin):
  """
  get_url(plugin)

  returns the download url for the specified plugin
  """
  sm_version = subprocess.check_output(
    'curl -s http://www.sourcemod.net/smdrop/1.7/sourcemod-latest-linux',
    shell=True,
  )

  download_url = {
    'metamod': 'http://www.metamodsource.net/mmsdrop/1.10/mmsource-1.10.7-git948-linux.tar.gz',
    'sourcemod': "http://www.sourcemod.net/smdrop/1.7/%s" % sm_version,
  }

  return download_url[plugin]


def install_dedicated_server(steam_path=None, game=None, sourcemod=False):
  """
  install_dedicated_server(steam_path=None, game=None, sourcemod=False)

  Executes the steamcmd script and begins downloading a dedicated server
  """
# Subtract one from the game to get the proper list index
  if game:
    game = int(game) - 1

    servers = [
      ('Counter-Strike Global Offensive', 740),
      ('Counter-Strike Source ', 232330),
      ('Day of Defeat Source', 232290),
      ('Garrys Mod', 4020),
      ('Insurgency', 237410),
      ('Left 4 Dead 2', 222860),
      ('Left 4 Dead', 22284),
      ('Team Fortress 2', 232250),
      ('Chivalry Medieval Warfare', 220070),
    ]

    # Replace spaces with underscores for friendly reading
  install_path = "%s_dedicated_server" % servers[game][0].replace(' ', '_')
  subprocess.call(
    "%s/steamcmd.sh +login anonymous +force_install_dir\
     \"%s/%s\" +app_update %s +quit" % (
      steam_path,
      steam_path,
      install_path,
      servers[game][1]
    ),
    shell=True)

  if sourcemod:
    # Addons go in the same directory that houses the cfg and maps dirs
    for root, dir, files in os.walk(
      "%s/%s" % (steam_path, install_path)
    ):
      if 'cfg' in dir and 'maps' in dir:
        download_plugins(game_path=root)
    print "Enjoy!"


def install_steamcmd(steamcmd_path=None):
  """
  install_steamcmd(steamcmd_path=None)

  Grabs the correct build of steamcmd for the paltform and unzips it
  """
  if os.path.exists("%s/steamcmd.sh" % steamcmd_path):
    print "Found existing steamcmd.sh install at %s" % steamcmd_path
    return

  if not os.path.exists(steamcmd_path):
    print "%s does not exist, creating path before downloading steamcmd\n"\
      % steamcmd_path
    os.makedirs(steamcmd_path)

  steamcmd_tar = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"

  downloaded_tar = "%s/steamcmd.tar.gz" % steamcmd_path

  print "Grabbing steamcmd from %s. Saving to %s\n" % (
    steamcmd_tar,
    downloaded_tar
  )

  subprocess.call(
    "wget --quiet -O %s %s" % (downloaded_tar, steamcmd_tar),
    shell=True
  )

  extract_file(compressed_file=downloaded_tar, target_path=steamcmd_path)


def download_plugins(game_path):
  """
  download_plugins(game_path)

  wgets the plugins
  """
  for plugin_name in ['metamod', 'sourcemod']:
    url = get_url(plugin=plugin_name)
    downloaded_plugin = "%s/%s" % (game_path, plugin_name)

    print "\nDownloading %s from %s\n" % (plugin_name, url)
    subprocess.call(
      "wget --quiet -O %s %s" % (downloaded_plugin, url), shell=True
    )

    # Extract the files
    extract_file(compressed_file=downloaded_plugin, target_path=game_path)


def parse_arguments():
  """
  parse_arguments()

  Parses the arguments passed to the script and calls appropriate functions
  """
  parser = argparse.ArgumentParser(
    description='Automate the installation of a SRCDS and metamod+sourcemod'
  )

  parser.add_argument(
    '--path',
    type=str,
    metavar='/home/steamuser/games',
    help='Target path to install game'
  )

  parser.add_argument(
    '--game',
    type=str,
    metavar='4',
    # required=True,
    help="Number of the game you wish to install\n\
          1. Counter-Strike Global Offensive\
          2. Counter-Strike Source \
          3. Day of Defeat Source\
          4. Garrys Mod\
          5. Insurgency\
          6. Left 4 Dead 2\
          7. Left 4 Dead\
          8. Team Fortress 2\
          9. Chivalry Medieval Warfare",
    choices=['1', '2', '3', '4', '5', '6', '7', '8', '9'],
  )

  parser.add_argument(
    '--sourcemod',
    action='store_true',
    help='Add this flag if you wish to install sourcemod and metamod'
  )

  args = parser.parse_args()

  install_steamcmd(steamcmd_path=args.path)

  install_dedicated_server(
    steam_path=args.path,
    game=args.game,
    sourcemod=args.sourcemod
  )

if __name__ == '__main__':
  parse_arguments()
