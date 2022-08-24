import logging

from ckan import plugins as p

log = logging.getLogger(__name__)


def harvest_source_delete(context, data_dict):
    '''Deletes an existing harvest source

    This method just proxies the request to package_delete,
    which will delete the actual harvest type dataset and the
    HarvestSource object (via the after_delete extension point).

    :param id: the name or id of the harvest source to delete
    :type id: string
    '''
    log.info('Deleting harvest source: %r', data_dict)
    p.toolkit.check_access('harvest_source_delete', context, data_dict)

    p.toolkit.get_action('package_delete')(context, data_dict)

    if context.get('clear_source', False):

        # We need the id. The name won't work.
        package_dict = p.toolkit.get_action('package_show')(context, data_dict)

        p.toolkit.get_action('harvest_source_clear')(
            context, {'id': package_dict['id']})
    #2021.12.2 add this in harvest_source_delete Func
    if context.get('completely_delete_resource', False):

        # We need the id. The name won't work.
        package_dict = p.toolkit.get_action('package_show')(context, data_dict)
        print("complete_delete:{}".format(package_dict))
        p.toolkit.get_action('complete_harvest_source_delete')(
            context, {'id': package_dict['id']})
