# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from composabl_core.agent.scenario.scenario import Scenario
from composabl_core.agent.skill.skill import Skill
from composabl_core.agent.skill.skill_coordinated import SkillCoordinated
from composabl_core.examples.demo_coordinated.agent import scenarios
from composabl_core.examples.demo_coordinated.agent.coach import (
    CoordinatedCoach,
)
from composabl_core.examples.demo_coordinated.agent.teacher import (
    IncrementTeacher,
)

increment_skill1 = Skill("skill1", IncrementTeacher)
increment_skill2 = Skill("skill2", IncrementTeacher)

coordinated_skill = SkillCoordinated("coordinated_skill", CoordinatedCoach, [
    increment_skill1, increment_skill2
])

for scenario_dict in scenarios:
    scenario = Scenario(scenario_dict)
    coordinated_skill.add_scenario(scenario)
