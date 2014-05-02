from django.core.management.base import BaseCommand
from optparse import make_option
from quintoandar_eb_deployer.app_settings import *
import subprocess
import os

class Command(BaseCommand):

	file_path = os.path.dirname(os.path.realpath(__file__))
	file_name = file_path + '/_awsElasticbeanstalkPush.py'

	option_list = BaseCommand.option_list + (
					make_option('--environment', '-e',
						help='Set deployment environment; Values: (producao|forno)'
					),
					make_option('--commit', '-c',
						help='Commit hash to rollback to'
					),
					make_option('--skip-static',
						action='store_true',
						default=False,
						help='Skip pushing static files'
					),
				)
  
	def handle(self, *args, **options):
		ENV = options.get('environment')
		COMMIT = options.get('commit')
		SKIP_STATIC = options.get('skip_static')
		ACCESS_KEY = EB_DEPLOYER_SETTINGS.get(ENV).get("ACCESS_KEY")
		SECRET_KEY = EB_DEPLOYER_SETTINGS.get(ENV).get("SECRET_KEY")
		REGION = EB_DEPLOYER_SETTINGS.get(ENV).get("REGION")
		ENVIRONMENT_NAME = EB_DEPLOYER_SETTINGS.get(ENV).get("ENVIRONMENT_NAME")
		APPLICATION_NAME = EB_DEPLOYER_SETTINGS.get(ENV).get("APPLICATION_NAME")
		
		if not ENV or (ENV != 'producao' and ENV != 'forno'):
			print 'Especify an environment: (producao|forno)'
			return
		
		print 'Deploying to: ' + ENV + '...'

		eb_update_command = [
			'python', 
			self.file_name, 
			'--access-key=' + ACCESS_KEY,
			'--secret-key=' + SECRET_KEY,
			'--region=' + REGION,
			'--environment-name=' + ENVIRONMENT_NAME,
			'--application-name=' + APPLICATION_NAME
		]
		if COMMIT:
			eb_update_command.append('--commit='+COMMIT)

		self.cmd(eb_update_command)

		if SKIP_STATIC:
			print 'Skiping static files...'
		else:
			print 'Compiling static files...'		
			os.chdir('search_py/static/minified')
			
			self.cmd(['./minifyStatic.sh', './GoogleClosure/compiler.jar', './YahooUIOptimizator/yuicompressor-2.4.7.jar'])

			print 'Pushing static files to S3...'
			if ENV == 'forno':
				self.cmd([
					'./s3cmd/s3cmd',
					'--dry-run',
					'--mime-type=application/x-javascript', 
					'-P',
					'--add-header="Cache-Control: max-age=60"', 
					'--add-header="Content-Encoding: gzip"',
					'sync', 	
					'./*_f.js.jgz', 
					's3://5ares/searchStatic/js/',
					'--config=../../../s3cmd.conf'
				])
				self.cmd([
					'./s3cmd/s3cmd',
					'--dry-run',
					'--mime-type=application/x-javascript', 
					'-P',
					'--add-header="Cache-Control: max-age=60"', 
					'--add-header="Content-Encoding: gzip"',
					'sync', 	
					'./*_f.js.jgz', 
					's3://5ares/searchStatic/js/',
					'--config=../../../s3cmd.conf'
				])

				#'./s3cmd/s3cmd --dry-run --mime-type=application/x-javascript -P --add-header="Cache-Control: max-age=60" --add-header="Content-Encoding: gzip" sync ./*_f.js.jgz s3://5ares/searchStatic/js/ --config=../../../s3cmd.conf'
			print 'Done pushing static files to S3!'

		print 'Done deploying to: ' + ENV + '!'

	def cmd(self, command, shell=False):

		#p = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#out, err = p.communicate()
		os.system(" ".join(command))
		#self.stdout.write(out)
		#if err:
			#print err.decode('utf-8')


