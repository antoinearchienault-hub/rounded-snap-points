
"""
Rounded Snap Points
IngeTrazo extension

Replaces square snapping indicators with circular dots.
"""

import views.viewport as vp_mod

QColor = vp_mod.QColor
QRectF = vp_mod.QRectF
Qt = vp_mod.Qt


class DotPainterProxy:
    def __init__(self, painter, rgb=None, radius=5.0):
        self._p = painter
        self._rgb = rgb
        self._radius = radius

    def __getattr__(self, name):
        return getattr(self._p, name)

    def drawRect(self, rect):
        cx = rect.center().x()
        cy = rect.center().y()
        r = self._radius

        if (
            self._rgb is not None
            and self._p.brush().style() != Qt.NoBrush
        ):
            self._p.setBrush(
                QColor.fromRgbF(
                    self._rgb[0],
                    self._rgb[1],
                    self._rgb[2],
                    0.85
                )
            )

        self._p.drawEllipse(
            QRectF(cx-r, cy-r, r*2, r*2)
        )


def setup(app):
    viewport = app.viewport
    ViewportClass = type(viewport)

    if not hasattr(ViewportClass, '_orig_draw_snap_indicator'):

        ViewportClass._orig_draw_snap_indicator = (
            ViewportClass._draw_snap_indicator
        )

        ViewportClass._orig_draw_inference_marker = (
            ViewportClass._draw_inference_marker
        )

        def patched_snap(self, painter, snap):
            rgb = getattr(snap, 'color', None)

            proxy = DotPainterProxy(
                painter, rgb, radius=5.0
            )

            return self._orig_draw_snap_indicator(
                proxy, snap
            )

        def patched_inference(self, painter):
            proxy = DotPainterProxy(
                painter, None, radius=5.0
            )

            return self._orig_draw_inference_marker(
                proxy
            )

        ViewportClass._draw_snap_indicator = patched_snap
        ViewportClass._draw_inference_marker = patched_inference

    viewport.update()
