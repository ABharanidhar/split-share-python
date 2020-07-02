import operator
import ast

import collections
from django.http import HttpResponseRedirect

from split.models import ResultDetail, PersonDetail, ShareDetail, GroupDetail


def store_object_in_group_details(owner, group_name, number_of_people):
    """
    Store group details to Group Detail table
    :param owner:
    :param group_name:
    :param number_of_people:
    :return:
    """
    try:
        group_detail = GroupDetail(owner=owner, group_name=group_name, number_of_people=number_of_people)
        group_detail.save()
    except Exception:
        return None
    return group_detail


def store_object_in_person_details_for_groups(group_detail, name, unit):
    """
    This method is used to store for Family/Group Details
    Store person details to Person Detail table
    :param group_detail:
    :param name:
    :param unit:
    :return:
    """
    person_detail = PersonDetail(group_id=group_detail, person_name=name, units_per_person=unit)
    person_detail.save()


def store_object_in_person_details_for_individuals(group_detail, name):
    """
    This method is used to store for Individual Details
    Store person details to Person Detail table
    :param group_detail:
    :param name:
    :return:
    """
    person_detail = PersonDetail(group_id=group_detail, person_name=name)
    person_detail.save()


def store_object_in_share_details(group_detail, description, total_price, shares):
    """
    Store result details to Share Detail table
    :param group_detail:
    :param description:
    :param total_price:
    :param shares:
    :return:
    """
    share_detail = ShareDetail(group_id=group_detail, description=description, total_price=total_price,
                               share_per_person=shares)
    share_detail.save()


def store_object_to_result_page(group_id, owe_to, owe_by, amount):
    """
    Store result details to Result Detail table
    :param group_id:
    :param owe_to:
    :param owe_by:
    :param amount:
    :return None:
    """
    group_detail = GroupDetail.objects.get(id=group_id)
    rd = ResultDetail(group_id=group_detail, owe_to=owe_to, owe_by=owe_by, amount=amount)
    rd.save()


def get_list_of_group_details_from_group_detail_for_current_user(owner):
    """
    Returns list of Group Details present in group from GroupDetail table for a particular User
    :param owner:
    :return group_details:
    """
    try:
        group_details = GroupDetail.objects.filter(owner=owner)
    except group_details.DoesNotExist:
        group_details = None
    return group_details


def get_object_from_group_detail_for_group_id(group_id):
    """
    Returns number of people present in group from GroupDetail table for a particular group id
    :param group_id:
    :return number_of_ppl:
    """

    try:
        group_detail = GroupDetail.objects.get(id=group_id)
    except GroupDetail.DoesNotExist:
        group_detail = None
    return group_detail


def delete_existing_data_in_share_detail_for_group_id(group_id):
    """
    Removing data from ResultDetail table for a particular group id
    :param group_id:
    :return:
    """
    ResultDetail.objects.filter(group_id=group_id).delete()
    return True


def get_list_of_person_names_from_person_detail_for_group_id(group_id):
    """
    Getting list of persons from PersonDetail table for a particular group id
    :param group_id:
    :return person_names:
    """
    person_names = list(PersonDetail.objects.filter(group_id=group_id).values_list('person_name', flat=True))

    return person_names


def get_all_data_from_share_detail_for_group_id(group_id):
    """
    getting complete share details form ShareDetail table for a particular group id
    :param group_id:
    :return share_details:
    """
    share_details = ShareDetail.objects.filter(group_id=group_id)
    if not share_details:
        return None
    else:
        return share_details


def get_all_data_from_person_detail_for_group_id(group_id):
    """
    getting complete person details form PersonDetail table for a particular group id
    :param group_id:
    :return person_details:
    """
    person_details = PersonDetail.objects.filter(group_id=group_id)
    if not person_details:
        return None
    else:
        return person_details


def share_calculation(group_id):
    """
    Performs the complete logic and store the results into Result table for furthur reference
    :param group_id:
    :return STATUS:
    :return ACK:
    """
    # getting complete share details form ShareDetail
    share_details = get_all_data_from_share_detail_for_group_id(group_id)

    if share_details is not None:

        # getting person names from PersonDetail
        # person_names = get_list_of_person_names_from_person_detail_for_group_id(group_id)
        person_details = get_all_data_from_person_detail_for_group_id(group_id)

        prices_list = list()
        totalprice_list = list()
        person_names = list()
        units_per_person = list()

        for person in person_details:
            person_names.append(person.person_name)
            units_per_person.append(person.units_per_person)

        # extracting string of numbers into list
        for share in share_details:
            prices_list.append(ast.literal_eval(share.share_per_person))
            totalprice_list.append(share.total_price)

        delete_existing_data_in_share_detail_for_group_id(group_id)

        # price_list, person_names
        number_of_people = len(person_names)  # number of people
        total_price = sum(totalprice_list)

        # new dynamic person changes
        total_units_of_people = 0
        for units in units_per_person:
            total_units_of_people = total_units_of_people + units

        per_individual_cost_list = list()
        for i in range(number_of_people):
            cost = (total_price * units_per_person[i]) / total_units_of_people
            per_individual_cost_list.append(cost)  # gets cost of each individual and stores in list
        prices_list_new = list()
        for new_list in prices_list:
            prices_list_new.append(list(map(int, new_list)))
        total_individual_spend = [sum(x) for x in zip(*prices_list_new)]  # cost spend by each individual
        # person_excess_spend = [x - per_individual_cost for x in
        #                        total_individual_spend]  # this shows person gets or sends from/to other +, -
        person_excess_spend = [x1 - x2 for (x1, x2) in zip(total_individual_spend, per_individual_cost_list)]

        # create a dictionary with personname:person_excess_spend
        dict_new = dict(zip(person_names, person_excess_spend))
        sorted_dict = collections.OrderedDict(sorted(dict_new.items(), key=operator.itemgetter(1), reverse=True))

        # again split them into two lists
        person_names_new = list(sorted_dict.keys())

        person_excess_spend_new = list(sorted_dict.values())

        # real calculation
        neg_index = 0
        pos_index = 0
        for value in person_excess_spend_new:
            if value >= 0:
                neg_index = neg_index + 1
            else:
                break

        while pos_index < neg_index < number_of_people:
            if person_excess_spend_new[pos_index] > (person_excess_spend_new[neg_index] * (-1)):
                store_object_to_result_page(group_id, person_names_new[pos_index], person_names_new[neg_index],
                                            person_excess_spend_new[neg_index] * (-1))
                person_excess_spend_new[pos_index] = person_excess_spend_new[pos_index] + person_excess_spend_new[
                    neg_index]
                person_excess_spend_new[neg_index] = 0
                neg_index = neg_index + 1
            elif person_excess_spend_new[pos_index] < (person_excess_spend_new[neg_index] * (-1)):
                store_object_to_result_page(group_id, person_names_new[pos_index], person_names_new[neg_index],
                                            person_excess_spend_new[pos_index])
                person_excess_spend_new[neg_index] = person_excess_spend_new[pos_index] + person_excess_spend_new[
                    neg_index]
                person_excess_spend_new[pos_index] = 0
                pos_index = pos_index + 1
            elif person_excess_spend_new[pos_index] == (person_excess_spend_new[neg_index] * (-1)):
                store_object_to_result_page(group_id, person_names_new[pos_index], person_names_new[neg_index],
                                            person_excess_spend_new[pos_index])
                person_excess_spend_new[pos_index] = 0
                person_excess_spend_new[neg_index] = 0
                pos_index = pos_index + 1
                neg_index = neg_index + 1
            else:
                return [False, "either failed or someone is trying to modify data/hack"]

        # final check that all vales are zero
        for value in person_excess_spend_new:
            if -1 > value > 1:
                return [False, "either zero_check_failed or someone is trying to modify data/hack"]
        # After all calculations
        return [True, "success"]
    else:
        return [False, "No Data Found"]
