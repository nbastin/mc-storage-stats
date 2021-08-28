# Copyright (c) 2021  Nick Bastin

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import anvil

SHULKERS = [
  "minecraft:shulker_box",
  "minecraft:white_shulker_box",
  "minecraft:orange_shulker_box",
  "minecraft:magenta_shulker_box",
  "minecraft:light_blue_shulker_box",
  "minecraft:yellow_shulker_box",
  "minecraft:lime_shulker_box",
  "minecraft:pink_shulker_box",
  "minecraft:gray_shulker_box",
  "minecraft:light_gray_shulker_box",
  "minecraft:cyan_shulker_box",
  "minecraft:purple_shulker_box",
  "minecraft:blue_shulker_box",
  "minecraft:brown_shulker_box",
  "minecraft:green_shulker_box",
  "minecraft:red_shulker_box",
  "minecraft:black_shulker_box",
  ]

STORAGE_IDS = [
  "minecraft:barrel",
  "minecraft:chest",
  "minecraft:dispenser",
  "minecraft:dropper",
  "minecraft:hopper",
  "minecraft:trapped_chest",
  ]
STORAGE_IDS.extend(SHULKERS)

POTIONS = [
  "minecraft:potion",
  "minecraft:lingering_potion",
  "minecraft:splash_potion"
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


def accumulate_slot_contents (slot, stuff):
    item_id = str(slot["id"])
    if item_id in POTIONS:
      stuff.setdefault("%s(%s)" % (item_id, str(slot["tag"]["Potion"])), [0])[0] += slot["Count"].value
    else:
      stuff.setdefault(item_id, [0])[0] += slot["Count"].value


def compute_shulker (slot, stuff):
  try:
    for sslot in slot["tag"]["BlockEntityTag"]["Items"]:
      accumulate_slot_contents(sslot, stuff)
  except KeyError:
    # Box has never been placed and has no slots
    pass


def compute_contents (te):
  stuff = {}
  try:
    for slot in te["Items"]:
      item_id = str(slot["id"])
      if item_id not in SHULKERS:
        accumulate_slot_contents(slot, stuff)
      else:
        stuff.setdefault(item_id, [0])[0] += 1
        compute_shulker(slot, stuff)
  except KeyError:
    if str(te["id"]) in SHULKERS:
      # Box has never been placed and has no slots
      pass
    else:
      print(te["id"], te["x"], te["y"], te["z"])
  return stuff

