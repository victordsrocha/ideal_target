from environment.simple_target import SimpleTarget


class Interface(object):

    def __init__(self, memory):
        self.env = SimpleTarget()
        self.memory = memory

    def enact(self, intended_interaction, step_actions_list):
        """
        recebe somente interações primitivas
        esta função deve "tentar" executar a interação intencionada no ambiente
        em seguida deve retornar a interação realmente executada (enacted)
        esta pode ou não ser igual à intencionada
        """
        result = None

        # intended_interaction.label[0]
        # label[0], ou seja, ^ > v, são as "primitive actions"
        # o restante da label é o "primitive feedback"
        # queremos executar uma primitive action no ambiente e receber um primitive feedback
        # e então juntá-las em uma única interação para comparar com o planejado
        act = intended_interaction.label[0]

        if act == '>':
            result = self.env.move()
        elif act == '^':
            result = self.env.left()
        elif act == 'v':
            result = self.env.right()

        enacted_interaction = self.memory.get_primitive_interaction(result)

        # print(enacted_interaction)
        # step_actions_list.append((enacted_interaction.label, self.m_x, self.m_y, self.m_o))
        # print(f'Posicao atual = {self.m_x},{self.m_y},{self.m_o}')
        return enacted_interaction
