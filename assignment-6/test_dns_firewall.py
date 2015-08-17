import random
import unittest
from ryu.lib.packet import dns
import dns_firewall


class TestDNSPolicy( unittest.TestCase ):

    def fake_transaction_id( self ):
        return random.randint(1, 1<<16)

    def fake_name( self ):
        return "fake%x.com" % random.randint(1, 1<<32)

    def fake_question( self, qtype = dns.dns.rr.A_TYPE ):
        return dns.dns.question( name   = self.fake_name(),
                                 qtype  = qtype,
                                 qclass = 1 )

    def fake_answer( self, question ):
        return dns.dns.rr( _name   = question.name,
                           _qtype  = question.qtype,
                           _qclass = question.qclass,
                           _ttl    = 3600,
                           _rdlen  = 4,
                           _rddata = 'xxxx' )

    def serialize_dns( self, d ):
        s = ''.join( [ ' ' for i in range( dns_firewall.DNS_OFFSET ) ] )
        s += d.serialize( None, None )
        return s

    def test_allow_queries( self ):

        # Send a single DNS question.
        # Expected:  question is allowed by firewall.

        d = dns.dns()
        d.id = self.fake_transaction_id()
        d.questions.append( self.fake_question() )
        kv = { "raw": self.serialize_dns( d ) }
        self.assertTrue( dns_firewall.dns_firewall( kv ) is not None )

    def test_valid_response( self ):

        # In this test, we will first send a DNS question once,
        # then send its answer twice.
        # Expected:  question and first answer allowed, second answer rejected.

        ques = self.fake_question()
        ans  = self.fake_answer( ques )

        # First send the request.
        d_ques = dns.dns()
        d_ques.id = self.fake_transaction_id()
        d_ques.questions.append( ques )
        kv_ques = { "raw": self.serialize_dns( d_ques ) }

        dns_firewall.dns_firewall( kv_ques )

        d_ans = dns.dns()
        d_ans.qr = True
        d_ans.id = d_ques.id
        d_ans.questions.append( ques )
        d_ans.answers.append( ans )
        kv_ans = { "raw": self.serialize_dns( d_ans ) }

        # Allow the response to go through once.
        self.assertTrue( dns_firewall.dns_firewall( kv_ans ) is not None )

        # Do not allow the response to go through a second time.
        self.assertTrue( dns_firewall.dns_firewall( kv_ans ) is None )

    def test_overlapping_requests( self ):

        # In this test, we will first send two DNS questions, then the DNS responses in 
        # reverse order
        # Expected:  question and answer allowed

        ques = self.fake_question()
        ans  = self.fake_answer( ques )

        # First send the request.
        d_ques = dns.dns()
        d_ques.id = self.fake_transaction_id()
        d_ques.questions.append( ques )
        kv1_ques = { "raw": self.serialize_dns( d_ques ) }

        d_ans = dns.dns()
        d_ans.qr = True
        d_ans.id = d_ques.id
        d_ans.questions.append( ques )
        d_ans.answers.append( ans )
        kv1_ans = { "raw": self.serialize_dns( d_ans ) }

        ques = self.fake_question()
        ans  = self.fake_answer( ques )

        # First send the request.
        d_ques = dns.dns()
        d_ques.id = self.fake_transaction_id()
        d_ques.questions.append( ques )
        kv2_ques = { "raw": self.serialize_dns( d_ques ) }

        d_ans = dns.dns()
        d_ans.qr = True
        d_ans.id = d_ques.id
        d_ans.questions.append( ques )
        d_ans.answers.append( ans )
        kv2_ans = { "raw": self.serialize_dns( d_ans ) }

        #
        # send the queries
        #
        self.assertTrue( dns_firewall.dns_firewall( kv1_ques ) is not None )
        self.assertTrue( dns_firewall.dns_firewall( kv2_ques ) is not None )

        # make sure both responses come back
        self.assertTrue( dns_firewall.dns_firewall( kv2_ans ) is not None )
        self.assertTrue( dns_firewall.dns_firewall( kv1_ans ) is not None )

    def test_repeating_requests( self ):

        # In this test, we will verify that the same request & response work if repeated
        # Expected:  question and answer allowed both times

        ques = self.fake_question()
        ans  = self.fake_answer( ques )

        # First send the request.
        d_ques = dns.dns()
        d_ques.id = self.fake_transaction_id()
        d_ques.questions.append( ques )
        kv1_ques = { "raw": self.serialize_dns( d_ques ) }

        d_ans = dns.dns()
        d_ans.qr = True
        d_ans.id = d_ques.id
        d_ans.questions.append( ques )
        d_ans.answers.append( ans )
        kv1_ans = { "raw": self.serialize_dns( d_ans ) }

        #
        # send the and the response for try 1
        #
        self.assertTrue( dns_firewall.dns_firewall( kv1_ques ) is not None )
        self.assertTrue( dns_firewall.dns_firewall( kv1_ans ) is not None )

        #
        # now for the second time
        #
        self.assertTrue( dns_firewall.dns_firewall( kv1_ques ) is not None )
        self.assertTrue( dns_firewall.dns_firewall( kv1_ans ) is not None )

    def test_valid_response_with_intermingled_fake_responses( self ):

        # In this test, we will first send a DNS question once,
        # then send its answer twice.
        # Expected:  question and first answer allowed, second answer rejected.

        ques = self.fake_question()
        ans  = self.fake_answer( ques )

        # First send the request.
        d_ques = dns.dns()
        d_ques.id = self.fake_transaction_id()
        d_ques.questions.append( ques )
        kv_ques = { "raw": self.serialize_dns( d_ques ) }

        dns_firewall.dns_firewall( kv_ques )

        d_ans = dns.dns()
        d_ans.qr = True
        d_ans.id = d_ques.id
        d_ans.questions.append( ques )
        d_ans.answers.append( ans )
        kv_ans = { "raw": self.serialize_dns( d_ans ) }

        #
        # try 10 fake responses
        #
        for i in range(0, 10) :
            ques = self.fake_question()
            ans  = self.fake_answer( ques )

            d_ans = dns.dns()
            d_ans.qr = True
            d_ans.id = self.fake_transaction_id()
            d_ans.questions.append( ques )
            d_ans.answers.append( ans )
            fake_ans = { "raw": self.serialize_dns( d_ans ) }

            self.assertTrue( dns_firewall.dns_firewall( fake_ans ) is None )

        # Allow the response to go through once.
        self.assertTrue( dns_firewall.dns_firewall( kv_ans ) is not None )

        # Do not allow the response to go through a second time.
        self.assertTrue( dns_firewall.dns_firewall( kv_ans ) is None )


    def test_spurious_response( self ):

        # Send a DNS answer for an unknown question.
        # Expected:  answer is rejected by firewall

        ques = self.fake_question()
        ans  = self.fake_answer( ques )

        d_ans = dns.dns()
        d_ans.qr = True
        d_ans.id = self.fake_transaction_id()
        d_ans.questions.append( ques )
        d_ans.answers.append( ans )
        kv_ans = { "raw": self.serialize_dns( d_ans ) }

        # Reject the response.
        self.assertTrue( dns_firewall.dns_firewall( kv_ans ) is None )


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDNSPolicy)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()

