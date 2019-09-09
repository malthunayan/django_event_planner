from rest_framework.permissions import BasePermission

class IsEventOwner(BasePermission):
	message = "You must be the owner of this event."

	def has_object_permission(self, request, view, obj):
		if request.user.is_staff or obj.user == request.user:
			return True
		return False

