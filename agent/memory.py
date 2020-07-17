from agent.interaction.experiment import Experiment
from agent.interaction.interaction import Interaction


class Memory:

    def __init__(self):
        self.known_interactions = {}
        self.known_experiments = {}
        self.init_simple_target()

    def add_or_get_composite_interaction(self, pre_interaction, post_interaction):
        label = '<' + pre_interaction.label + post_interaction.label + '>'

        if label not in self.known_interactions.keys():
            interaction = self.add_or_get_interaction(label)
            interaction.pre_interaction = pre_interaction
            interaction.post_interaction = post_interaction
            interaction.valence = pre_interaction.valence + post_interaction.valence
            self.add_or_get_abstract_experiment(interaction)
        else:
            interaction = self.known_interactions[label]

        return interaction

    def add_or_get_and_reinforce_composite_interaction(self, pre_interaction, post_interaction):
        composite_interaction = self.add_or_get_composite_interaction(pre_interaction, post_interaction)
        composite_interaction.weight += 1
        '''
        if composite_interaction.weight == 1:
            print(f'learn {composite_interaction}')
        else:
            print(f'reinforce {composite_interaction}')
        '''
        return composite_interaction

    # somente por questão de controle todas as criações de novas interações passam por aqui
    def add_or_get_interaction(self, label):
        if label not in self.known_interactions.keys():
            self.known_interactions[label] = Interaction(label)
        return self.known_interactions[label]

    def add_or_get_abstract_experiment(self, interaction):
        label = interaction.label.replace('e', 'E').replace('r', 'R').replace('>', '|')
        if label not in self.known_experiments:
            abstract_experiment = Experiment(label)
            abstract_experiment.intended_interaction = interaction
            interaction.experiment = abstract_experiment
            self.known_experiments[label] = abstract_experiment
        return self.known_experiments[label]

    def add_primitive_interaction(self, label):
        if label not in self.known_interactions.keys():
            interaction = self.add_or_get_interaction(label)
            interaction.valence = self.calc_valence(label)
        interaction = self.known_interactions[label]
        return interaction

    def get_primitive_interaction(self, label):
        return self.known_interactions[label]

    def calc_valence(self, label):

        # TODO criar um controle mais fácil para alterar
        # valores de preferência sem precisar vir até aqui

        sum_valence = 0
        sum_valence += label.count('^') * 0
        sum_valence += label.count('>') * 0
        sum_valence += label.count('v') * 0
        sum_valence += label.count('.') * 0
        sum_valence += label.count('w') * (-5)
        sum_valence += label.count('*') * 15
        sum_valence += label.count('+') * 10
        sum_valence += label.count('x') * 15
        sum_valence += label.count('o') * (-15)
        return sum_valence

    def init_simple_target(self):

        # seria bom automatizar essa criação de interações primitivas
        # para facilitar a tarefa em projetos maiores

        l1 = self.add_primitive_interaction("^w**")
        l2 = self.add_primitive_interaction("^w+*")
        l3 = self.add_primitive_interaction("^wx*")
        l4 = self.add_primitive_interaction("^wo*")
        l5 = self.add_primitive_interaction("^w*+")
        l6 = self.add_primitive_interaction("^w++")
        l7 = self.add_primitive_interaction("^wx+")
        l8 = self.add_primitive_interaction("^wo+")
        l9 = self.add_primitive_interaction("^w*x")
        l10 = self.add_primitive_interaction("^w+x")
        l11 = self.add_primitive_interaction("^wxx")
        l12 = self.add_primitive_interaction("^wox")
        l13 = self.add_primitive_interaction("^w*o")
        l14 = self.add_primitive_interaction("^w+o")
        l15 = self.add_primitive_interaction("^wxo")
        l16 = self.add_primitive_interaction("^woo")
        l17 = self.add_primitive_interaction("^.**")
        l18 = self.add_primitive_interaction("^.+*")
        l19 = self.add_primitive_interaction("^.x*")
        l20 = self.add_primitive_interaction("^.o*")
        l21 = self.add_primitive_interaction("^.*+")
        l22 = self.add_primitive_interaction("^.++")
        l23 = self.add_primitive_interaction("^.x+")
        l24 = self.add_primitive_interaction("^.o+")
        l25 = self.add_primitive_interaction("^.*x")
        l26 = self.add_primitive_interaction("^.+x")
        l27 = self.add_primitive_interaction("^.xx")
        l28 = self.add_primitive_interaction("^.ox")
        l29 = self.add_primitive_interaction("^.*o")
        l30 = self.add_primitive_interaction("^.+o")
        l31 = self.add_primitive_interaction("^.xo")
        l32 = self.add_primitive_interaction("^.oo")
        r1 = self.add_primitive_interaction("vw**")
        r2 = self.add_primitive_interaction("vw+*")
        r3 = self.add_primitive_interaction("vwx*")
        r4 = self.add_primitive_interaction("vwo*")
        r5 = self.add_primitive_interaction("vw*+")
        r6 = self.add_primitive_interaction("vw++")
        r7 = self.add_primitive_interaction("vwx+")
        r8 = self.add_primitive_interaction("vwo+")
        r9 = self.add_primitive_interaction("vw*x")
        r10 = self.add_primitive_interaction("vw+x")
        r11 = self.add_primitive_interaction("vwxx")
        r12 = self.add_primitive_interaction("vwox")
        r13 = self.add_primitive_interaction("vw*o")
        r14 = self.add_primitive_interaction("vw+o")
        r15 = self.add_primitive_interaction("vwxo")
        r16 = self.add_primitive_interaction("vwoo")
        r17 = self.add_primitive_interaction("v.**")
        r18 = self.add_primitive_interaction("v.+*")
        r19 = self.add_primitive_interaction("v.x*")
        r20 = self.add_primitive_interaction("v.o*")
        r21 = self.add_primitive_interaction("v.*+")
        r22 = self.add_primitive_interaction("v.++")
        r23 = self.add_primitive_interaction("v.x+")
        r24 = self.add_primitive_interaction("v.o+")
        r25 = self.add_primitive_interaction("v.*x")
        r26 = self.add_primitive_interaction("v.+x")
        r27 = self.add_primitive_interaction("v.xx")
        r28 = self.add_primitive_interaction("v.ox")
        r29 = self.add_primitive_interaction("v.*o")
        r30 = self.add_primitive_interaction("v.+o")
        r31 = self.add_primitive_interaction("v.xo")
        r32 = self.add_primitive_interaction("v.oo")
        m1 = self.add_primitive_interaction(">w**")
        m2 = self.add_primitive_interaction(">w+*")
        m3 = self.add_primitive_interaction(">wx*")
        m4 = self.add_primitive_interaction(">wo*")
        m5 = self.add_primitive_interaction(">w*+")
        m6 = self.add_primitive_interaction(">w++")
        m7 = self.add_primitive_interaction(">wx+")
        m8 = self.add_primitive_interaction(">wo+")
        m9 = self.add_primitive_interaction(">w*x")
        m10 = self.add_primitive_interaction(">w+x")
        m11 = self.add_primitive_interaction(">wxx")
        m12 = self.add_primitive_interaction(">wox")
        m13 = self.add_primitive_interaction(">w*o")
        m14 = self.add_primitive_interaction(">w+o")
        m15 = self.add_primitive_interaction(">wxo")
        m16 = self.add_primitive_interaction(">woo")
        m17 = self.add_primitive_interaction(">.**")
        m18 = self.add_primitive_interaction(">.+*")
        m19 = self.add_primitive_interaction(">.x*")
        m20 = self.add_primitive_interaction(">.o*")
        m21 = self.add_primitive_interaction(">.*+")
        m22 = self.add_primitive_interaction(">.++")
        m23 = self.add_primitive_interaction(">.x+")
        m24 = self.add_primitive_interaction(">.o+")
        m25 = self.add_primitive_interaction(">.*x")
        m26 = self.add_primitive_interaction(">.+x")
        m27 = self.add_primitive_interaction(">.xx")
        m28 = self.add_primitive_interaction(">.ox")
        m29 = self.add_primitive_interaction(">.*o")
        m30 = self.add_primitive_interaction(">.+o")
        m31 = self.add_primitive_interaction(">.xo")
        m32 = self.add_primitive_interaction(">.oo")

        # alguns experimentos podem ser descobertos pelo próprio agente
        # depois tentar retirar alguns casos, especialmente as "falhas"

        self.add_or_get_abstract_experiment(l1)
        self.add_or_get_abstract_experiment(l2)
        self.add_or_get_abstract_experiment(l3)
        self.add_or_get_abstract_experiment(l4)
        self.add_or_get_abstract_experiment(l5)
        self.add_or_get_abstract_experiment(l6)
        self.add_or_get_abstract_experiment(l7)
        self.add_or_get_abstract_experiment(l8)
        self.add_or_get_abstract_experiment(l9)
        self.add_or_get_abstract_experiment(l10)
        self.add_or_get_abstract_experiment(l11)
        self.add_or_get_abstract_experiment(l12)
        self.add_or_get_abstract_experiment(l13)
        self.add_or_get_abstract_experiment(l14)
        self.add_or_get_abstract_experiment(l15)
        self.add_or_get_abstract_experiment(l16)
        self.add_or_get_abstract_experiment(l17)
        self.add_or_get_abstract_experiment(l18)
        self.add_or_get_abstract_experiment(l19)
        self.add_or_get_abstract_experiment(l20)
        self.add_or_get_abstract_experiment(l21)
        self.add_or_get_abstract_experiment(l22)
        self.add_or_get_abstract_experiment(l23)
        self.add_or_get_abstract_experiment(l24)
        self.add_or_get_abstract_experiment(l25)
        self.add_or_get_abstract_experiment(l26)
        self.add_or_get_abstract_experiment(l27)
        self.add_or_get_abstract_experiment(l28)
        self.add_or_get_abstract_experiment(l29)
        self.add_or_get_abstract_experiment(l30)
        self.add_or_get_abstract_experiment(l31)
        self.add_or_get_abstract_experiment(l32)
        self.add_or_get_abstract_experiment(r1)
        self.add_or_get_abstract_experiment(r2)
        self.add_or_get_abstract_experiment(r3)
        self.add_or_get_abstract_experiment(r4)
        self.add_or_get_abstract_experiment(r5)
        self.add_or_get_abstract_experiment(r6)
        self.add_or_get_abstract_experiment(r7)
        self.add_or_get_abstract_experiment(r8)
        self.add_or_get_abstract_experiment(r9)
        self.add_or_get_abstract_experiment(r10)
        self.add_or_get_abstract_experiment(r11)
        self.add_or_get_abstract_experiment(r12)
        self.add_or_get_abstract_experiment(r13)
        self.add_or_get_abstract_experiment(r14)
        self.add_or_get_abstract_experiment(r15)
        self.add_or_get_abstract_experiment(r16)
        self.add_or_get_abstract_experiment(r17)
        self.add_or_get_abstract_experiment(r18)
        self.add_or_get_abstract_experiment(r19)
        self.add_or_get_abstract_experiment(r20)
        self.add_or_get_abstract_experiment(r21)
        self.add_or_get_abstract_experiment(r22)
        self.add_or_get_abstract_experiment(r23)
        self.add_or_get_abstract_experiment(r24)
        self.add_or_get_abstract_experiment(r25)
        self.add_or_get_abstract_experiment(r26)
        self.add_or_get_abstract_experiment(r27)
        self.add_or_get_abstract_experiment(r28)
        self.add_or_get_abstract_experiment(r29)
        self.add_or_get_abstract_experiment(r30)
        self.add_or_get_abstract_experiment(r31)
        self.add_or_get_abstract_experiment(r32)
        self.add_or_get_abstract_experiment(m1)
        self.add_or_get_abstract_experiment(m2)
        self.add_or_get_abstract_experiment(m3)
        self.add_or_get_abstract_experiment(m4)
        self.add_or_get_abstract_experiment(m5)
        self.add_or_get_abstract_experiment(m6)
        self.add_or_get_abstract_experiment(m7)
        self.add_or_get_abstract_experiment(m8)
        self.add_or_get_abstract_experiment(m9)
        self.add_or_get_abstract_experiment(m10)
        self.add_or_get_abstract_experiment(m11)
        self.add_or_get_abstract_experiment(m12)
        self.add_or_get_abstract_experiment(m13)
        self.add_or_get_abstract_experiment(m14)
        self.add_or_get_abstract_experiment(m15)
        self.add_or_get_abstract_experiment(m16)
        self.add_or_get_abstract_experiment(m17)
        self.add_or_get_abstract_experiment(m18)
        self.add_or_get_abstract_experiment(m19)
        self.add_or_get_abstract_experiment(m20)
        self.add_or_get_abstract_experiment(m21)
        self.add_or_get_abstract_experiment(m22)
        self.add_or_get_abstract_experiment(m23)
        self.add_or_get_abstract_experiment(m24)
        self.add_or_get_abstract_experiment(m25)
        self.add_or_get_abstract_experiment(m26)
        self.add_or_get_abstract_experiment(m27)
        self.add_or_get_abstract_experiment(m28)
        self.add_or_get_abstract_experiment(m29)
        self.add_or_get_abstract_experiment(m30)
        self.add_or_get_abstract_experiment(m31)
        self.add_or_get_abstract_experiment(m32)
