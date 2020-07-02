import ast

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from split import properties
from split.forms import CalculationForm
from split.operations import share_calculation, \
    get_object_from_group_detail_for_group_id, store_object_in_group_details, \
    get_list_of_group_details_from_group_detail_for_current_user, store_object_in_share_details, \
    get_list_of_person_names_from_person_detail_for_group_id, get_all_data_from_person_detail_for_group_id, \
    store_object_in_person_details_for_groups, store_object_in_person_details_for_individuals
from .models import GroupDetail, PersonDetail, ShareDetail, ResultDetail


@login_required()
def index(request):
    template_name = 'split/index.html'
    groups = get_list_of_group_details_from_group_detail_for_current_user(request.user)
    return render(request, template_name, {'groups': groups})


@login_required
def edit(request, group_id):
    return HttpResponse(properties.TEMPORARY_UNAVAILABLE)


@login_required
def create(request):
    template_name = 'split/creategroup.html'
    return render(request, template_name)


def error_view(request):
    return HttpResponse(properties.TEMPORARY_UNAVAILABLE)


@login_required
def create_group(request):
    if request.method == 'POST':

        group_name = request.POST['group_name']
        number_of_people = int(request.POST['number_of_people'])
        i = 1
        names = list()
        while True:
            name = "person_" + str(i)
            if name in request.POST:
                names.append(request.POST[name])
                i = i + 1
            else:
                break

        # storing into database
        group_detail = store_object_in_group_details(request.user, group_name, number_of_people)

        if group_detail is not None:
            for i in range(number_of_people):
                store_object_in_person_details_for_individuals(group_detail, names[i])
        else:
            error_message = 'Error at Storing Group Details. Please try again..!'
            template_name = 'split/creategroup.html'
            context = {'error_messages': error_message}
            return render(request, template_name, context)

        return HttpResponseRedirect('/split/')

    else:

        template_name = 'split/creategroup.html'
        return render(request, template_name)


@login_required
def create_groups(request):
    if request.method == 'POST':

        group_name = request.POST['group_name']
        number_of_people = int(request.POST['number_of_people'])
        i = 1
        names = list()
        while True:
            name = "person_" + str(i)
            if name in request.POST:
                names.append(request.POST[name])
                i = i + 1
            else:
                break

        i = 1
        units = list()
        while True:
            name = "unit_" + str(i)
            if name in request.POST:
                units.append(int(request.POST[name]))
                i = i + 1
            else:
                break

        # storing into database
        group_detail = store_object_in_group_details(request.user, group_name, number_of_people)

        if group_detail is not None:
            for i in range(number_of_people):
                store_object_in_person_details_for_groups(group_detail, names[i], units[i])
        else:
            error_message = 'Error at Storing Group Details. Please try again..!'
            template_name = 'split/creategroup.html'
            context = {'error_messages': error_message}
            return render(request, template_name, context)

        return HttpResponseRedirect('/split/')

    else:

        template_name = 'split/creategroups.html'
        return render(request, template_name)


@login_required
def open_group(request, group_id):
    """ When a group is opened this method is called.
        For the first time, empty form is created
    """
    group_detail = get_object_from_group_detail_for_group_id(group_id)

    if group_detail:
        number_of_ppl = group_detail.number_of_people
        form = CalculationForm(number_of_ppl)
        form.fields['group_id'].initial = group_id
        form.fields['number_of_ppl'].initial = group_detail.number_of_people
        person_details = get_all_data_from_person_detail_for_group_id(group_id)
        person_names = list()
        units_per_person = list()
        for person in person_details:
            person_names.append(person.person_name)
            units_per_person.append(person.units_per_person)

        flag = False
        for unit in units_per_person:
            if unit > 1:
                flag = True
                break
        if flag:
            for i in range(number_of_ppl):
                form.fields['person_%s' % (i + 1)].label = person_names[i]
                form.fields['person_%s' % (i + 1)].help_text = str(units_per_person[i])+' members(s)'
        else:
            for i in range(number_of_ppl):
                form.fields['person_%s' % (i + 1)].label = person_names[i]

        share_details = ShareDetail.objects.filter(group_id=group_id).order_by('-last_updated')
        for share in share_details:
            share.prices_list = ast.literal_eval(share.share_per_person)
        return render(request, 'split/main.html',
                      {'group_detail': group_detail, 'form': form, 'share_details': share_details,
                       'person_names': person_names, 'group_id': group_id})
    else:
        return HttpResponse("Something went wrong..!")


def ajax_share_data_insert(request):
    if request.method == 'POST':
        group_id = request.POST['group_id']
        description = request.POST['description']
        total_price = request.POST['total_price']
        shares = request.POST.getlist('share[]')
        group_detail = get_object_from_group_detail_for_group_id(group_id)
        store_object_in_share_details(group_detail, description, total_price, shares)

        url = '/split/open/' + str(group_id) + '/'
        return HttpResponseRedirect(url)

    else:
        # request is GET that means something is wrong
        return HttpResponseRedirect('/split/error_view')


@login_required
def delete_group(request, group_id):
    # GroupDetail.objects.filter(id=group_id).delete()
    return HttpResponseRedirect('/split/')


@login_required
def calculations(request, group_id):
    data = share_calculation(group_id)
    if data[0]:
        result_details = ResultDetail.objects.filter(group_id=group_id)
        template_name = 'split/result.html'
        context = {'result_details': result_details}
        return render(request, template_name, context)
    else:
        return HttpResponse(data[1])
