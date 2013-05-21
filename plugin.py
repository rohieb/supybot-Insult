# vim:set fileencoding=utf-8
###
# Copyright (c) 2004-2005, Mike Taylor
# Copyright (c) 2009, Roland Hieber
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import random

class Insult(callbacks.Plugin):
    def _buildInsult(self):
        """
        Insults are formed by making combinations of:
        You are nothing but a(n) {adj} {amt} of {adj} {noun}
        """
        if self.registryValue('allowFoul'):
            _nouns = self.registryValue('nouns') + \
                     self.registryValue('foulNouns')
            _amounts = self.registryValue('amounts') + \
                       self.registryValue('foulAmounts')
            _adjectives = self.registryValue('adjectives') + \
                          self.registryValue('foulAdjectives')
        else:
            _nouns = self.registryValue('nouns')
            _amounts = self.registryValue('amounts')
            _adjectives = self.registryValue('adjectives')
        adj1 = utils.iter.choice(_adjectives)
        adj2 = utils.iter.choice(_adjectives)
        noun = utils.iter.choice(_nouns)
        amount = utils.iter.choice(_amounts)
        if adj1 == adj2:
            adj2 = utils.iter.choice(_adjectives)
        if not adj1[0] in 'aeiou':
            an = 'a'
        else:
            an = 'an'
        return format('You are nothing but %s %s %s of %s %s.',
                      an, adj1, amount, adj2, noun)

    def insult(self, irc, msg, args, victim):
        """[<target>]

        Reply optionally directed at a random string, person,
        object, etc.
        """
        tempinsult = self._buildInsult()
        if not victim:
            irc.reply(tempinsult, prefixNick=False)
        else:
            irc.reply(format('%s - %s ', victim, tempinsult),
                      prefixNick=False)
    insult = wrap(insult, [additional('text')])

    def slap(self, irc, msg, args, victim):
        """<victim>

        Slaps <victim>. Or something like that.
        """

        random.seed()
        if random.randint(1,500) == 30:
          irc.reply("I'm tired punishing people. Do this yourself.")
          return

        actions = ['slaps','bats','bricks','beats','slashes at','strikes at',
            'strikes','slams','smacks','smites','socks','punches','@bites',
            '@drops an anvil on','@removes %s stomach with a pair of scissors',
            '@ties %n to a rock and trains an eagle to eat from %s liver',
            'removes %s heart','@kills','@kicks','@inflates %n until he bursts',
            '@tickles %n until he dies laughing','@throws small pebbles at',
            '@throws a rock at','@stones','@pelts %n with uncooked peas',
            '@squirts lemon juice at %n','tortures','@fries %n in hot oil',
            "@decides that it's time to hug %n once again",'@sets a dog on %n',
            'tortures %n kind of dreadfully','makes %n fail on his next exam',
            '@installs Windows on %s computer','deletes %s hard disk',
            '@hides %s toothbrush','@hands %n an ignited firecracker',
            '@ties up %s shoelaces','removes %s eyelids',
            '@punches %n in the face',
            '@makes %n addictive to drugs and lets the problem solve itself'
            ]
        adverbs = ['almost','heavily','slowly','softly','angrily',
            'unsuccessfully']
        additions = ['','','with a large trout','with a herring',
            'with a red herring','with an anvil','with a crowbar',
            'by dropping an anvil on his head','with a hammer',
            "with Joejoearmani's Gummihämmer(TM)",'but fails at it',
            'with the handle of a lollypop','with a small teaspoon'
            ]

        rply = utils.iter.choice(actions)
        advb = utils.iter.choice(adverbs)
        addn = utils.iter.choice(additions);

        # replace %'s or add victim
        if (rply.find("%n") == -1 and rply.find("%s") == -1):
            rply = rply + ' ' + victim
        else:
            # replace %n by victim
            rply = rply.replace("%n", victim)
            # replace %s by victim's genitive
            if victim.endswith('s') or victim.endswith('z'):
                rply = rply.replace("%s", victim + "'")
            else:
                rply = rply.replace("%s", victim + "'s")

        if rply.startswith('@'):
            # action without addition
            rply = rply.lstrip('@')
        else:
            # action with addition
            rply = rply + ' ' + addn

        # sometimes add adverb
        if random.randint(0,10) > 8:
          rply = advb + ' ' + rply

        # finally reply
        irc.reply(rply, action=True)
    slap = wrap(slap, ['text'])

Class = Insult

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
