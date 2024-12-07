from osbot_utils.base_classes.Type_Safe import Type_Safe

from osbot_aws.aws.ecs.ECS import ECS
from osbot_aws.aws.ecs.ECS_Fargate_Task import ECS_Fargate_Task
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


class CBR__Fargate(Type_Safe):
    cluster_name : str
    image_name   : str

    @cache_on_self
    def ecs(self):
        return ECS()

    def cluster(self):
        cluster_arn = self.ecs().cluster_arn(self.cluster_name)
        return self.ecs().cluster(cluster_arn=cluster_arn)

    def task(self):
        task_definition_arn = 'arn:aws:ecs:eu-west-1:654654216424:task-definition/task__cbr_website_beta:1'
        task                = ECS_Fargate_Task(cluster_name=self.cluster_name, image_name=self.image_name)
        task.task_family    = task_definition_arn
        return task

    def task_logs(self, task_arn, task_definition_arn):
        kwargs_logs = dict(task_arn            = task_arn                ,
                           task_definition_arn = task_definition_arn     ,
                           image_name          = self.image_name         ,
                           cluster_name        = self.cluster_name )
        return self.ecs().logs(**kwargs_logs)

    def tasks(self):
        return self.ecs().tasks(self.cluster_name)