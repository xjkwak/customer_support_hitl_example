from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from customer_support_hitl_example.models import TicketInfo
from customer_support_hitl_example.tools.db_tool import SaveTicketTool
from customer_support_hitl_example.tools.human_tool import HumanInputContextTool


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CustomerSupportHitlExample():
	"""CustomerSupportHitlExample crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	# @agent
	# def ticket_analyzer(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['ticket_analyzer'],
	# 		verbose=True
	# 	)

	@agent
	def information_collector(self) -> Agent:
		human_tool = HumanInputContextTool()
		return Agent(
			config=self.agents_config['information_collector'],
			tools=[human_tool],
			verbose=True
		)

	@agent
	def information_summarizer(self) -> Agent:
		return Agent(
			config=self.agents_config['information_summarizer'],
			tools=[SaveTicketTool()],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	# @task
	# def analyze_ticket_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['analyze_ticket_task'],
	# 	)

	@task
	def collect_info_task(self) -> Task:
		return Task(
			config=self.tasks_config['collect_info_task'],
			output_json=TicketInfo,
		)

	@task
	def summarize_ticket_task(self) -> Task:
		return Task(
			config=self.tasks_config['summarize_ticket_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CustomerSupportHitlExample crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
