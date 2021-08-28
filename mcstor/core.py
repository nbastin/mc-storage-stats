# Copyright (c) 2021  Nick Bastin

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import anvil

STORAGE_IDS = [
  "minecraft:chest",
  "minecraft:barrel",
  "minecraft:trapped_chest",
#  "minecraft:shulker_box",
#  "minecraft:light_gray_shulker_box",
  ]

class ChunkStreamer():
  def __init__ (self, region_dir, chunk_csv_path):
    self._region_dir = region_dir
    self._chunk_csv = chunk_csv_path

    self._chunk_pos_by_region = {}

    self._load()

  def _load (self):
    with open(self._chunk_csv, "r") as chf:
      for row in chf:
        # MCASelector has a funny idea of what a comma is
        p = [int(x) for x in row.split(";")]
        self._chunk_pos_by_region.setdefault((p[0], p[1]), []).append((p[2], p[3]))

  def __iter__ (self):
    for rA,rB in self._chunk_pos_by_region:
      path = "%s/r.%d.%d.mca" % (self._region_dir, rA, rB)
      region = anvil.Region.from_file(path)
      for chunk_pos in self._chunk_pos_by_region[(rA, rB)]:
        yield anvil.Chunk.from_region(region, chunk_pos[0], chunk_pos[1])


class StorageEntityStreamer():
  def __init__ (self, chunk):
    self._chunk = chunk

  def __iter__ (self):
    for te in self._chunk.tile_entities:
      if str(te["id"]) in STORAGE_IDS:
        yield te


def compute_contents (te):
  stuff = {}
  try:
    for slot in te["Items"]:
      stuff.setdefault(str(slot["id"]), [0])[0] += slot["Count"].value
  except KeyError:
    print(te["id"], te["x"], te["y"], te["z"])
  return stuff

