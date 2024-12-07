from pathlib import Path

from musurgia.fractal import FractalTree
from musurgia.fractal.graphic import GraphicTree
from musurgia.pdf import Pdf, draw_ruler, TextLabel, DrawObjectColumn
from musurgia.tests.utils_for_tests import PdfTestCase, create_test_fractal_tree, add_node_infos_to_graphic

path = Path(__file__)


class TestCreatLayerGraphic(PdfTestCase):
    def setUp(self):
        self.ft = create_test_fractal_tree()
        self.pdf = Pdf(orientation='l')

    def test_create_layer_graphic(self):
        unit = 24
        gt = GraphicTree(self.ft, unit=unit, distance=12, shrink_factor=0.6)
        add_node_infos_to_graphic(self.ft, gt)

        graphic = gt.get_graphic()
        graphic.bottom_margin = 30

        graphic_layer_2 = gt.create_layer_graphic(layer_number=2)
        graphic_layer_2.add_text_label(
            TextLabel(value='layer 2', placement='left', font_size=8, right_margin=2))
        graphic_layer_2.bottom_margin = 20

        graphic_layer_3 = gt.create_layer_graphic(layer_number=3)
        graphic_layer_3.add_text_label(
            TextLabel(value='layer 3', placement='left', font_size=8, right_margin=2))

        c = DrawObjectColumn()

        c.add_draw_object(graphic)
        c.add_draw_object(graphic_layer_2)
        c.add_draw_object(graphic_layer_3)

        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, 'h', unit=unit, first_label=-1)
            draw_ruler(self.pdf, 'v', unit=unit)
            self.pdf.translate(unit, 10)
            c.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
