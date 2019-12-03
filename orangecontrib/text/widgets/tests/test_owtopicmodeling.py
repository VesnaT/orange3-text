import unittest

import numpy as np
from AnyQt.QtCore import QItemSelectionModel

from Orange.widgets.tests.base import WidgetTest
from orangecontrib.text.corpus import Corpus
from orangecontrib.text.widgets.owtopicmodeling import OWTopicModeling


class TestTopicModeling(WidgetTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.corpus = Corpus.from_file('deerwester')

    def setUp(self):
        self.widget = self.create_widget(OWTopicModeling)

    def test_data(self):
        def until():
            return bool(self.get_output(self.widget.Outputs.selected_topic))

        self.send_signal(self.widget.Inputs.corpus, self.corpus)
        self.process_events(until)

        self.send_signal(self.widget.Inputs.corpus, None)
        output = self.get_output(self.widget.Outputs.selected_topic)
        self.assertIsNone(output)

    def test_saved_selection(self):
        def until(widget=self.widget):
            return bool(self.get_output(widget.Outputs.selected_topic))

        self.send_signal(self.widget.Inputs.corpus, self.corpus)
        self.process_events(until)
        idx = self.widget.topic_desc.model().index(2, 0)
        self.widget.topic_desc.selectionModel().select(
            idx, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)
        output1 = self.get_output(self.widget.Outputs.selected_topic)
        state = self.widget.settingsHandler.pack_data(self.widget)

        w = self.create_widget(OWTopicModeling, stored_settings=state)
        self.send_signal(w.Inputs.corpus, self.corpus, widget=w)
        self.process_events(lambda: until(w))
        output2 = self.get_output(w.Outputs.selected_topic, widget=w)
        np.testing.assert_allclose(output1, output2)


if __name__ == "__main__":
    unittest.main()
