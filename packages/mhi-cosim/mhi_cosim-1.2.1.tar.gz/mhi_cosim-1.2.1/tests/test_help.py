import unittest
import mhi.cosim


class TestHelp(unittest.TestCase):
    
    def test_module(self):
        # Documentation should have an example using a `with` statement
        self.assertIn('with mhi.cosim.cosimulation(', mhi.cosim.__doc__)
    
    def test_cosimulation(self):
        # Documentation should have an example using a `with` statement
        self.assertIn('with mhi.cosim.cosimulation(',
                      mhi.cosim.cosimulation.__doc__)
    
    def test_channel(self):
        # Should talk about `channel_id`
        self.assertIn('`channel_id`', mhi.cosim.Channel.__doc__)
    
    def test_channel_send(self):
        # Should talk about sending to a remote
        self.assertIn('stored values', mhi.cosim.Channel.send.__doc__)
        self.assertIn('remote end', mhi.cosim.Channel.send.__doc__)
    
    def test_channel_get_value(self):
        # Should talk about blocking
        self.assertIn('will block', mhi.cosim.Channel.get_value.__doc__)

    def test_channel_get_values(self):
        # Should talk about blocking
        self.assertIn('will block', mhi.cosim.Channel.get_values.__doc__)

    def test_channel_read_only_attrs(self):
        self.assertIn('read-only', mhi.cosim.Channel.id.__doc__)
        self.assertIn('read-only', mhi.cosim.Channel.recv_size.__doc__)
        self.assertIn('read-only', mhi.cosim.Channel.send_size.__doc__)

if __name__ == '__main__':
    unittest.main()
