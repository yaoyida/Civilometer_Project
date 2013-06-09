from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView, ListView, DetailView

from django.views.generic.simple import redirect_to
import settings
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    #Public pages
    url(r'^$', TemplateView.as_view(template_name="public/home.html")),
    url(r'^how-it-works/$', TemplateView.as_view(template_name="public/how-it-works.html")),
	url(r'^play-with-data/$', TemplateView.as_view(template_name="public/play-with-data.html")),
	url(r'^get-involved/$', TemplateView.as_view(template_name="public/get-involved.html")),
	url(r'^definitions/$', 'cvm_app.views.public.definitions'),
	url(r'^definitions/([0-9]+)/.*?/$', 'cvm_app.views.public.definition'),
	url(r'^gallery/$', TemplateView.as_view(template_name="public/gallery.html")),

    #Public: Ajax
    url(r'^ajax/sign-in/$', 'cvm_app.views.public.signin'),
    url(r'^sign-out/$', 'cvm_app.views.public.signout'),

    #Admin

    #Admin: Object list pages
	url(r'^admin/$', 'cvm_app.views.admin.admin'),
	url(r'^admin/users/$', 'cvm_app.views.admin.users'),
	url(r'^admin/codebooks/$', 'cvm_app.views.admin.codebooks'),
	url(r'^admin/collections/$', 'cvm_app.views.admin.collections'),
	url(r'^admin/batches/$', 'cvm_app.views.admin.batches'),

    #Admin: Object view pages
    url(r'^user/(.*)/$', 'cvm_app.views.admin.user'),
    url(r'^codebook/(.*)/$', 'cvm_app.views.admin.codebook'),
    url(r'^collection/(.*)/$', 'cvm_app.views.admin.collection'),
    url(r'^batch/(.*)/$', 'cvm_app.views.admin.batch'),

    url(r'^batch/(.*)/export/$', 'cvm_app.views.admin.export_batch'),  #?

    #Admin: Ajax
    url(r'^ajax/create-account/$', 'cvm_app.views.admin.create_account'),
    url(r'^ajax/update-account/$', 'cvm_app.views.admin.update_account'),
    url(r'^ajax/update-permission/$', 'cvm_app.views.admin.update_permission'),

    url(r'^ajax/upload-collection/$', 'cvm_app.views.admin.upload_collection'),
    url(r'^ajax/upload-document/$', 'cvm_app.views.admin.upload_document'),
    url(r'^ajax/create-collection/$', 'cvm_app.views.admin.create_collection'),
    url(r'^ajax/get-collection-docs/$', 'cvm_app.views.admin.get_collection_docs'),
    url(r'^ajax/update-collection/$', 'cvm_app.views.admin.update_collection'),
    url(r'^ajax/import-collection/$', 'cvm_app.views.admin.import_collection'),
    url(r'^ajax/update-meta-data/$', 'cvm_app.views.admin.update_meta_data'),

    url(r'^ajax/import-codebook/$', 'cvm_app.views.admin.import_codebook'),
    url(r'^ajax/get-codebook/$', 'cvm_app.views.admin.get_codebook'),
    url(r'^ajax/save-codebook/$', 'cvm_app.views.admin.save_codebook'),
    url(r'^ajax/update-codebook/$', 'cvm_app.views.admin.update_codebook'),

    url(r'^ajax/start-batch/$', 'cvm_app.views.admin.start_batch'),
    url(r'^ajax/update-batch-reliability/$', 'cvm_app.views.admin.update_batch_reliability'),
    url(r'^ajax/submit-batch-code/$', 'cvm_app.views.admin.submit_batch_code'),
    url(r'^ajax/compile-batch/$', 'cvm_app.views.admin.compile_batch'),

    #Tasks:
    (r'^tasks/$', redirect_to, {'url' : '/tasks/choose-task/'}),
    url(r'^tasks/choose-task/$', 'cvm_app.views.task.choose_task'),
    url(r'^tasks/all-done/(.*)/$', 'cvm_app.views.task.task_all_done'),
    url(r'^tasks/game-session/(.*)/$', 'cvm_app.views.task.task'),
    url(r'^tasks/mturk/$', 'cvm_app.views.task.mturk'),
    url(r'^tasks/mturk-instructions/$', TemplateView.as_view(template_name="tasks/mturk-instructions.html")),

    #Tasks: Ajax:
    url(r'^tasks/ajax/create-game-session/$', 'cvm_app.views.task.create_game_session'),
    url(r'^tasks/ajax/get-first-task/$', 'cvm_app.views.task.get_first_task'),
    url(r'^tasks/ajax/submit-task/$', 'cvm_app.views.task.submit_task'),
    url(r'^tasks/ajax/quit-game-session/$', 'cvm_app.views.task.quit_game_session'),

    #url(r'^tasks/ajax/get-tasks-list/$', 'cvm_app.views.get_tasks_list'),
    #url(r'^tasks/ajax/sumbit-task-codes/$', 'cvm_app.views.submit_task_codes'),

    #APIs:
    url(r'^api/query-count/$', 'cvm_app.views.api.query_count'),
    url(r'^api/mapreduce-query/$', 'cvm_app.views.api.mapreduce_query'),
    

    # Examples:
    # url(r'^$', 'cvm_project.views.home', name='home'),
    # url(r'^cvm_project/', include('cvm_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),

    #(r'^test-route/$', 'cvm_app.views.task.test_route'),

)

