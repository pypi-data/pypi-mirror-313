# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from composabl_core.agent.agent import Agent
from composabl_core.agent import SkillGroup
from composabl_core.examples.demo.agent import (
    target_skill_box,
    target_skill_dictionary,
    target_skill_discrete,
    target_skill_multi_binary,
    target_skill_multi_discrete,
    target_skill_nested_scenario,
    target_skill_tuple,
    target_skill_text,
    target_skill_custom_action_space,
    target_skill_remote,
    expert_skill_controller_box,
    pass_through_skill_controller,
    dummy_skill_controller,
    sensors_dict,
    mapped_sensors_dict
)

agent_dictionary = Agent()
agent_dictionary.add_sensors(mapped_sensors_dict["dictionary"])
agent_dictionary.add_skill(target_skill_dictionary)

agent_box = Agent()
agent_box.add_sensors(mapped_sensors_dict["box"])
agent_box.add_skill(target_skill_box)

agent_discrete = Agent()
agent_discrete.add_sensors(mapped_sensors_dict["discrete"])
agent_discrete.add_skill(target_skill_discrete)

agent_multidiscrete = Agent()
agent_multidiscrete.add_sensors(mapped_sensors_dict["multidiscrete"])
agent_multidiscrete.add_skill(target_skill_multi_discrete)

agent_multibinary = Agent()
agent_multibinary.add_sensors(mapped_sensors_dict["multibinary"])
agent_multibinary.add_skill(target_skill_multi_binary)

agent_tuple = Agent()
agent_tuple.add_sensors(mapped_sensors_dict["tuple"])
agent_tuple.add_skill(target_skill_tuple)

agent_nested_scenario = Agent()
agent_nested_scenario.add_sensors(mapped_sensors_dict["dictionary"])
agent_nested_scenario.add_skill(target_skill_nested_scenario)

agent_setpoint = Agent()
agent_setpoint.add_sensors(mapped_sensors_dict["discrete"])
agent_setpoint.add_skill(target_skill_custom_action_space)
agent_setpoint.add_skill(pass_through_skill_controller)
skill_group = SkillGroup(target_skill_custom_action_space, pass_through_skill_controller)
agent_setpoint.add_skill_group(skill_group=skill_group)

agent_controller_drl = Agent()
agent_controller_drl.add_sensors(mapped_sensors_dict["discrete"])
agent_controller_drl.add_skill(target_skill_custom_action_space)
agent_controller_drl.add_skill(pass_through_skill_controller)
skill_group = SkillGroup(pass_through_skill_controller, target_skill_custom_action_space)
agent_controller_drl.add_skill_group(skill_group=skill_group)

agent_controller = Agent()
agent_controller.add_skill(expert_skill_controller_box)
agent_controller.add_sensors(mapped_sensors_dict["box"])

agent_text = Agent()
agent_text.add_skill(target_skill_text)
agent_text.add_sensors(mapped_sensors_dict["text"])


mapped_agents_for_space = {
    "box": agent_box,
    "dictionary": agent_dictionary,
    "discrete": agent_discrete,
    "multidiscrete": agent_multidiscrete,
    "multibinary": agent_multibinary,
    "tuple": agent_tuple,
    "set_point": agent_setpoint,
    "controller_box": agent_controller,
    "text": agent_text,
    "controller_drl_skill_group": agent_controller_drl
}

agent_dictionary = Agent()
agent_dictionary.add_sensors(sensors_dict["dictionary"])
agent_dictionary.add_skill(target_skill_dictionary)

agent_box = Agent()
agent_box.add_sensors(sensors_dict["box"])
agent_box.add_skill(target_skill_box)

agent_discrete = Agent()
agent_discrete.add_sensors(sensors_dict["discrete"])
agent_discrete.add_skill(target_skill_discrete)

agent_multidiscrete = Agent()
agent_multidiscrete.add_sensors(sensors_dict["multidiscrete"])
agent_multidiscrete.add_skill(target_skill_multi_discrete)

agent_multibinary = Agent()
agent_multibinary.add_sensors(sensors_dict["multibinary"])
agent_multibinary.add_skill(target_skill_multi_binary)

agent_tuple = Agent()
agent_tuple.add_sensors(sensors_dict["tuple"])
agent_tuple.add_skill(target_skill_tuple)

agent_nested_scenario = Agent()
agent_nested_scenario.add_sensors(sensors_dict["dictionary"])
agent_nested_scenario.add_skill(target_skill_nested_scenario)

agent_setpoint = Agent()
agent_setpoint.add_sensors(sensors_dict["discrete"])
agent_setpoint.add_skill(target_skill_custom_action_space)
agent_setpoint.add_skill(pass_through_skill_controller)
skill_group = SkillGroup(target_skill_custom_action_space, pass_through_skill_controller)
agent_setpoint.add_skill_group(skill_group=skill_group)

agent_controller_drl = Agent()
agent_controller_drl.add_sensors(sensors_dict["discrete"])
agent_controller_drl.add_skill(target_skill_custom_action_space)
agent_controller_drl.add_skill(dummy_skill_controller)
skill_group = SkillGroup(dummy_skill_controller, target_skill_custom_action_space)
agent_controller_drl.add_skill_group(skill_group=skill_group)

agent_controller = Agent()
agent_controller.add_skill(expert_skill_controller_box)
agent_controller.add_sensors(sensors_dict["box"])

agent_text = Agent()
agent_text.add_skill(target_skill_text)
agent_text.add_sensors(sensors_dict["text"])

agent_remote = Agent()
agent_remote.add_skill(target_skill_remote)
agent_remote.add_sensors(sensors_dict["dictionary"])

agents_for_space = {
    "box": agent_box,
    "dictionary": agent_dictionary,
    "discrete": agent_discrete,
    "multidiscrete": agent_multidiscrete,
    "multibinary": agent_multibinary,
    "tuple": agent_tuple,
    "set_point": agent_setpoint,
    "controller_box": agent_controller,
    "text": agent_text,
    "controller_drl_skill_group": agent_controller_drl,
    "remote": agent_remote
}
