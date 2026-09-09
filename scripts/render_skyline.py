#!/usr/bin/env python3
"""Render a gh-skyline STL into a rotating animation for the profile README.

Rasterises the mesh with a stochastic-sample painter's algorithm: every triangle
is splatted with a number of barycentric samples proportional to its projected
area, then samples are drawn far-to-near so nearer geometry wins. Fully
vectorised with numpy, so a full turntable renders in seconds.

Palette is Catppuccin Mocha.
"""

from __future__ import annotations

import argparse
import struct
from pathlib import Path

import numpy as np
from PIL import Image

# --- Catppuccin Mocha -------------------------------------------------------
BASE = (30, 30, 46)  # #1e1e2e
CRUST = (17, 17, 27)  # #11111b
MAUVE = (203, 166, 247)  # #cba6f7
BLUE = (137, 180, 250)  # #89b4fa
SAPPHIRE = (116, 199, 236)  # #74c7ec
TEAL = (148, 226, 213)  # #94e2d5
SURFACE = (49, 50, 68)  # #313244


def load_stl(path: Path) -> np.ndarray:
    """Return an (n, 3, 3) float32 array of triangle vertices."""
    raw = path.read_bytes()
    # Binary STL: 80-byte header, uint32 count, then 50 bytes per facet.
    count = struct.unpack("<I", raw[80:84])[0]
    expected = 84 + count * 50
    if expected != len(raw):
        raise ValueError(f"{path}: not a binary STL (expected {expected} bytes, got {len(raw)})")
    rec = np.frombuffer(raw, dtype=np.uint8, count=count * 50, offset=84).reshape(count, 50)
    # Bytes 12..48 of each facet are the three vertices; skip the normal and the
    # trailing uint16 attribute count.
    verts = rec[:, 12:48].copy().view(np.float32).reshape(count, 3, 3)
    return verts


def normalise(tris: np.ndarray) -> np.ndarray:
    """Centre the model on the origin and scale it into a unit-ish box."""
    flat = tris.reshape(-1, 3)
    lo, hi = flat.min(axis=0), flat.max(axis=0)
    centre = (lo + hi) / 2.0
    # Keep the model sitting on z = 0 so it reads as a city on a plate.
    centre[2] = lo[2]
    scale = 2.0 / max(hi[0] - lo[0], hi[1] - lo[1])
    return (tris - centre) * scale


def rotation(yaw: float, pitch: float) -> np.ndarray:
    cy, sy = np.cos(yaw), np.sin(yaw)
    cp, sp = np.cos(pitch), np.sin(pitch)
    rz = np.array([[cy, -sy, 0.0], [sy, cy, 0.0], [0.0, 0.0, 1.0]])
    rx = np.array([[1.0, 0.0, 0.0], [0.0, cp, -sp], [0.0, sp, cp]])
    return rx @ rz


def shade(normals: np.ndarray, height: np.ndarray) -> np.ndarray:
    """Flat shading: a height ramp tinted by a key light and a cool fill."""
    key = np.array([0.45, -0.55, 0.70])
    key /= np.linalg.norm(key)
    lam = np.clip(normals @ key, 0.0, 1.0)
    fill = np.clip(normals @ np.array([-0.6, 0.25, 0.30]), 0.0, 1.0)

    # Ramp from a dark plinth at ground level up through sapphire to mauve, so
    # the base plate recedes and the contribution towers carry the colour.
    t = np.clip(height, 0.0, 1.0)[:, None]
    low = np.array(SURFACE, dtype=float)[None, :]
    mid = np.array(SAPPHIRE, dtype=float)[None, :]
    high = np.array(MAUVE, dtype=float)[None, :]
    k = np.clip(t / 0.16, 0.0, 1.0)
    base = low * (1 - k) + mid * k
    k2 = np.clip((t - 0.16) / 0.84, 0.0, 1.0)
    base = base * (1 - k2) + high * k2

    lit = base * (0.32 + 0.60 * lam[:, None]) + np.array(BLUE)[None, :] * 0.16 * fill[:, None]
    return np.clip(lit, 0, 255)


def reference_span(tris: np.ndarray, yaws: np.ndarray) -> float:
    """Widest projected footprint across the sweep, so zoom stays constant."""
    flat = tris.reshape(-1, 3)
    x0, y0 = flat[:, 0].min(), flat[:, 1].min()
    x1, y1 = flat[:, 0].max(), flat[:, 1].max()
    corners = np.array([[x0, y0], [x1, y0], [x0, y1], [x1, y1]])
    widest = 0.0
    for yaw in yaws:
        px = corners[:, 0] * np.cos(yaw) - corners[:, 1] * np.sin(yaw)
        widest = max(widest, float(px.max() - px.min()))
    return widest


def render(
    tris: np.ndarray, yaw: float, width: int, height: int, ref_span: float, ss: int = 2
) -> Image.Image:
    W, H = width * ss, height * ss
    # Negative pitch tilts the camera above the horizon, so model +z (building
    # height) climbs up the screen and the top faces stay visible.
    rot = rotation(yaw, np.radians(-64.0))

    pts = tris @ rot.T  # (n, 3, 3)

    # Face normals in view space, from the original winding.
    e0 = pts[:, 1] - pts[:, 0]
    e1 = pts[:, 2] - pts[:, 0]
    nrm = np.cross(e0, e1)
    ln = np.linalg.norm(nrm, axis=1)
    ok = ln > 1e-12
    pts, nrm, ln = pts[ok], nrm[ok], ln[ok]
    nrm = nrm / ln[:, None]

    # Backface cull: the camera looks down -z after rotation.
    front = nrm[:, 2] > 0.0
    pts, nrm = pts[front], nrm[front]
    if len(pts) == 0:
        return Image.new("RGB", (width, height), CRUST)

    # Orthographic projection, fitted to the frame by bounding box. The zoom is
    # taken from a fixed reference span (the yaw-invariant model diagonal) so
    # the model does not pulse in size as the turntable rotates.
    xy = pts[:, :, :2]
    x0, x1 = xy[:, :, 0].min(), xy[:, :, 0].max()
    y0, y1 = xy[:, :, 1].min(), xy[:, :, 1].max()
    zoom = min(0.94 * W / max(ref_span, 1e-9), 0.92 * H / max(y1 - y0, 1e-9))
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    sx = (xy[:, :, 0] - cx) * zoom + W / 2.0
    sy = H / 2.0 - (xy[:, :, 1] - cy) * zoom
    sz = pts[:, :, 2]

    # Model-space height drives the colour ramp.
    zmodel = tris[ok][front][:, :, 2].mean(axis=1)
    zmodel = (zmodel - zmodel.min()) / max(np.ptp(zmodel), 1e-9)
    colours = shade(nrm, zmodel)

    # Samples per triangle, proportional to projected area.
    area = 0.5 * np.abs(
        (sx[:, 1] - sx[:, 0]) * (sy[:, 2] - sy[:, 0])
        - (sx[:, 2] - sx[:, 0]) * (sy[:, 1] - sy[:, 0])
    )
    # No upper cap: the base plate is a handful of enormous triangles and
    # clipping their sample count is what riddles it with holes.
    nsamp = np.clip(np.ceil(area * 2.6).astype(np.int64), 1, None)
    total = int(nsamp.sum())
    idx = np.repeat(np.arange(len(nsamp)), nsamp)

    # Per-triangle sample ordinal, then a Hammersley pair mapped onto the
    # triangle. Stratified beats i.i.d. random here: uniform coverage at ~1
    # sample per pixel instead of the holes random sampling leaves behind.
    starts = np.concatenate(([0], np.cumsum(nsamp)[:-1]))
    j = np.arange(total, dtype=np.int64) - np.repeat(starts, nsamp)
    n_i = nsamp[idx]

    r1 = (j + 0.5) / n_i
    bits = j.astype(np.uint64)
    bits = ((bits & np.uint64(0x5555555555555555)) << np.uint64(1)) | (
        (bits & np.uint64(0xAAAAAAAAAAAAAAAA)) >> np.uint64(1)
    )
    bits = ((bits & np.uint64(0x3333333333333333)) << np.uint64(2)) | (
        (bits & np.uint64(0xCCCCCCCCCCCCCCCC)) >> np.uint64(2)
    )
    bits = ((bits & np.uint64(0x0F0F0F0F0F0F0F0F)) << np.uint64(4)) | (
        (bits & np.uint64(0xF0F0F0F0F0F0F0F0)) >> np.uint64(4)
    )
    bits = ((bits & np.uint64(0x00FF00FF00FF00FF)) << np.uint64(8)) | (
        (bits & np.uint64(0xFF00FF00FF00FF00)) >> np.uint64(8)
    )
    bits = ((bits & np.uint64(0x0000FFFF0000FFFF)) << np.uint64(16)) | (
        (bits & np.uint64(0xFFFF0000FFFF0000)) >> np.uint64(16)
    )
    bits = (bits << np.uint64(32)) | (bits >> np.uint64(32))
    r2 = bits.astype(np.float64) / 2.0**64

    s = np.sqrt(r1)
    w = 1.0 - s
    u = r2 * s
    v = (1.0 - r2) * s

    px = sx[idx, 0] * w + sx[idx, 1] * u + sx[idx, 2] * v
    py = sy[idx, 0] * w + sy[idx, 1] * u + sy[idx, 2] * v
    pz = sz[idx, 0] * w + sz[idx, 1] * u + sz[idx, 2] * v

    xi = np.rint(px).astype(np.int64)
    yi = np.rint(py).astype(np.int64)
    inside = (xi >= 0) & (xi < W) & (yi >= 0) & (yi < H)
    xi, yi, pz, idx = xi[inside], yi[inside], pz[inside], idx[inside]

    # Painter's algorithm: draw far samples first so near ones overwrite.
    order = np.argsort(pz, kind="stable")
    flat = yi[order] * W + xi[order]

    canvas = np.empty((H * W, 3), dtype=np.float32)
    canvas[:] = np.array(CRUST, dtype=np.float32)
    canvas[flat] = colours[idx[order]].astype(np.float32)

    img = Image.fromarray(canvas.reshape(H, W, 3).astype(np.uint8), "RGB")
    return img.resize((width, height), Image.LANCZOS)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stl", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--frames", type=int, default=1)
    ap.add_argument("--width", type=int, default=900)
    ap.add_argument("--height", type=int, default=420)
    ap.add_argument("--yaw", type=float, default=0.0, help="degrees, for a single still")
    ap.add_argument("--sweep", type=float, default=360.0, help="degrees covered by the loop")
    ap.add_argument("--duration", type=int, default=90, help="ms per frame")
    ap.add_argument("--ss", type=int, default=3, help="supersampling factor")
    args = ap.parse_args()

    tris = normalise(load_stl(args.stl))
    print(f"{args.stl.name}: {len(tris):,} triangles")

    if args.frames <= 1:
        yaws = np.array([np.radians(args.yaw)])
        span = reference_span(tris, yaws)
        render(tris, yaws[0], args.width, args.height, span, args.ss).save(args.out)
        print(f"wrote {args.out}")
        return

    # Ping-pong the turntable with a cosine ease instead of spinning a full
    # circle: a skyline viewed from behind reads as a wall, and the eased
    # reversal loops seamlessly without a visible seam.
    half = args.frames // 2
    t = np.arange(half) / half
    swing = np.radians(args.sweep / 2.0) * -np.cos(np.pi * t)
    yaws = np.radians(args.yaw) + np.concatenate([swing, swing[::-1]])

    span = reference_span(tris, yaws)
    frames = []
    for i, yaw in enumerate(yaws):
        frames.append(render(tris, yaw, args.width, args.height, span, args.ss))
        print(f"  frame {i + 1}/{len(yaws)}", flush=True)

    frames[0].save(
        args.out,
        save_all=True,
        append_images=frames[1:],
        duration=args.duration,
        loop=0,
        optimize=True,
    )
    print(f"wrote {args.out} ({args.out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
