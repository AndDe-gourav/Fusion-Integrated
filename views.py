from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Employee, LeaveCategory, Entitlement, LeaveApplication, LeaveApplicationTransition

@csrf_exempt
def create_leave_application(request):
    if request.method == 'POST':
        data = request.POST
        employee = Employee.objects.get(user=request.user)
        leave_category = LeaveCategory.objects.get(name=data['leave_category'])
        start_date = data['start_date']
        end_date = data['end_date']
        purpose = data['purpose']

        application = LeaveApplication(
            employee=employee,
            leave_category=leave_category,
            start_date=start_date,
            end_date=end_date,
            purpose=purpose,
            status='draft'
        )
        application.save()

        transition = LeaveApplicationTransition(
            application=application,
            status='submitted'
        )
        transition.save()

        return JsonResponse({'message': 'Leave application created successfully'}, status=201)

@csrf_exempt
def update_leave_application(request, application_id):
    if request.method == 'PUT':
        data = request.POST
        application = LeaveApplication.objects.get(id=application_id)
        application.status = data['status']
        application.save()

        transition = LeaveApplicationTransition(
            application=application,
            status=data['status'],
            transitioned_at=datetime.now()
        )
        transition.save()

        return JsonResponse({'message': 'Leave application updated successfully'}, status=200)

@csrf_exempt
def get_leave_application(request, application_id):
    application = LeaveApplication.objects.get(id=application_id)
    transitions = LeaveApplicationTransition.objects.filter(application=application)
    return JsonResponse({
        'id': application.id,
        'employee': application.employee.user.username,
        'leave_category': application.leave_category.name,
        'start_date': application.start_date,
        'end_date': application.end_date,
        'purpose': application.purpose,
        'status': application.status,
        'transitions': [{'status': transition.status, 'transitioned_at': transition.transitioned_at} for transition in transitions]
    }, status=200)
