from rest_framework import serializers


class TaskStatusAnalyticsSerializer(serializers.Serializer):
    todo = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    done = serializers.IntegerField()
    total = serializers.IntegerField()


class ProjectTaskAnalyticsSerializer(serializers.Serializer):
    project_id = serializers.UUIDField()
    project_name = serializers.CharField()
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    completion_percentage = serializers.FloatField()


class UserTaskAnalyticsSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    username = serializers.CharField()
    total_tasks_assigned = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    in_progress_tasks = serializers.IntegerField()
    completion_rate = serializers.FloatField()
