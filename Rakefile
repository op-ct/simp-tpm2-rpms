require 'rake'
require 'fileutils'
require 'rake/clean'
require 'yaml'

if Rake.verbose
  include FileUtils::Verbose
else
  include FileUtils
end

rake_file = File.expand_path *Rake.application.find_rakefile_location
rake_file = File.realpath(rake_file) if File.symlink?(rake_file)
yaml_file = File.join(File.dirname(rake_file),'things_to_build.yaml')
@things_to_download = YAML.load_file yaml_file


def dl_untar(url,dst)
  mkdir_p dst
  Dir.chdir dst
  sh "curl -sSfL '#{url}' | tar zxvf -"
end

def git_clone(url,ref,dst)
  sh "git clone '#{url}' -b '#{ref}' '#{dst}'"
end


def dl( dl_info, dir )
  Dir.chdir File.dirname(dir)
  url = dl_info[:url].gsub('%{TAG}',dl_info[:tag])
  if File.directory? dir
    warn "WARNING: path '#{dir}' exists; aborting download"
    return dir
  end
  case dl_info[:type]
  when :targz
    dl_untar url, dir
  when :gitrepo
    git_clone url, dl_info[:tag], dir
  else
    fail "ERROR: :type is not :targz or :gitrepo (#{dl_info.inspect})"
  end
  dir
end



def tar_gz key, thing, dst
  _parent, _dir = File.dirname(dst), File.basename(dst)
  cwd = Dir.pwd
  Dir.chdir(_parent)
  sh "tar zcvf '#{_dir}.tar.gz' '#{_dir}'"
  Dir.chdir cwd
end



def build key, thing, dist_dir
end


def spec_info spec_file
  info = {}
  cmd="rpm -q --define 'debug_package %{nil}' --queryformat '%{NAME} %{VERSION} %{RELEASE} %{ARCH}\n' --specfile '#{spec_file}'"
  cmd="rpm -q --define 'debug_package %{nil}' --queryformat '%{NAME} %{VERSION} %{RELEASE} %{ARCH}\n' --specfile '#{spec_file}'"
  info[:basename], info[:version], info[:release], info[:arch] = %x{#{cmd}}.strip.split
  info[:full_name]="#{info[:basename]}-#{info[:version]}-#{info[:release]}"
  info[:ver_name]="#{info[:basename]}-#{info[:version]}"
  info
end

CLEAN << 'dist'

def define_tasks
  cwd = Dir.pwd
  dist_dir = File.expand_path('dist')
  dist_rpmbuild_dir = File.expand_path('dist/rpmbuild')
  logs_dir = File.expand_path('tmp/logs',dist_dir)
  dist_rpmbuild_sources_dir = File.expand_path('SOURCES',dist_rpmbuild_dir)
  dist_rpmbuild_build_dir = File.expand_path('BUILD',dist_rpmbuild_dir)
  dist_rpmbuild_buildroot_dir = File.expand_path('BUILDROOT',dist_rpmbuild_dir)
  extra_sources_dir = File.expand_path('extra_sources',dist_dir)
  Dir[ '*.spec' ].each do |spec|
    spec_path = File.expand_path(spec)
    info = spec_info(spec)
    dl_dir = File.expand_path("dist/#{info[:ver_name]}")

    namespace :src do
      directory dist_dir
      directory dist_rpmbuild_sources_dir
      directory dist_rpmbuild_build_dir
      directory dist_rpmbuild_buildroot_dir
      directory logs_dir
      directory extra_sources_dir

      desc 'downloads source'
      task :download => [dist_dir, dist_rpmbuild_sources_dir] do
	mkdir_p File.join(dist_dir,'tmp','logs')
        mkdir_p dist_rpmbuild_buildroot_dir
        mkdir_p dist_rpmbuild_build_dir
        mkdir_p dist_rpmbuild_sources_dir
        mkdir_p extra_sources_dir
        dl_info = @things_to_download[info[:basename]]

        # download the source0
        dl(dl_info, dl_dir)

        # download extras (source1, etc)
        cmds = dl_info.fetch(:extras,{}).fetch(:post_dl,[])
        cmds.each{ |cmd| sh cmd.gsub('%{SOURCES_DIR}',extra_sources_dir) }
      end
    end
    namespace :pkg do
      desc 'builds RPM'
      task :rpm => 'src:download' do
        Dir.chdir File.dirname(dl_dir)
        tar_file = File.join(dist_rpmbuild_sources_dir, "#{info[:ver_name]}.tar.gz")
        puts "===================================== TAR ============================\n" * 7
        # Build process got cranky without .git to reference
        ###tar_cmd='tar --owner 0 --group 0 --exclude-vcs ' \
        tar_cmd='tar --owner 0 --group 0 ' \
                "-cpzf #{tar_file} #{File.basename dl_dir}"
        sh tar_cmd
        puts "------------------- cp -r #{File.join(extra_sources_dir,'.')} #{dist_rpmbuild_sources_dir}"
        FileUtils.cp_r(File.join(extra_sources_dir,'.'), dist_rpmbuild_sources_dir)

        # Something buried in some builds responds to the env var and not the macro
        ENV['RPM_BUILD_ROOT']=dist_rpmbuild_buildroot_dir

        puts "===================================== SRPM ============================\n" * 7
        srpm_cmd="rpmbuild -D 'debug_package %{nil}' "\
                "-D 'buildroot #{dist_rpmbuild_buildroot_dir}' " \
                "-D '_builddir #{dist_rpmbuild_build_dir}' " \
                "-D '_sourcedir #{dist_rpmbuild_sources_dir}' " \
                "-D '_rpmdir #{dist_dir}' -D '_srcrpmdir #{dist_dir}' " \
                "-D '_build_name_fmt %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm' " \
                " -v -bs #{spec_path} " \
                "|& tee #{logs_dir}/build.srpm.log"
       sh srpm_cmd


       Dir.chdir cwd
puts "===================================== RPM ============================\n" * 7
       rpm_cmd="rpmbuild --define 'debug_package %{nil}' " \
               "-D 'buildroot #{dist_rpmbuild_buildroot_dir}' " \
               "-D '_builddir #{dist_rpmbuild_build_dir}' " \
               "-D '_sourcedir #{dist_rpmbuild_sources_dir}' " \
               "-D '_rpmdir #{dist_dir}' -D '_srcrpmdir #{dist_dir}' " \
               "-D '_build_name_fmt %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm' " \
               " -v -ba #{spec_path}  " \
               "|& tee #{logs_dir}/build.rpm.log"
#               "> #{logs_dir}/build.rpm.out 2> #{logs_dir}/build.rpm.err"

File.open(File.join(cwd,'rpm.sh'),'w'){|f| f.puts rpm_cmd }
        sh rpm_cmd
      end
    end
  end
end






define_tasks



namespace :upstream do
  task :do_all do
    do_all
  end
end


task :tar do
end

