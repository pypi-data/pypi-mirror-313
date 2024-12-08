# argument version

set -eux

while getopts "v:" opt; do
  case $opt in
    v)
      version=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

if [ -z "$version" ]; then
  echo "version is required"
  exit 1
fi

export PYTHONPATH=$PWD pytest tests

docker build -f Docker/Evaluate.Dockerfile . -t bigcodebench/bigcodebench-evaluate:$version
docker tag bigcodebench/bigcodebench-evaluate:$version bigcodebench/bigcodebench-evaluate:latest
docker push bigcodebench/bigcodebench-evaluate:$version
docker push bigcodebench/bigcodebench-evaluate:latest

docker build -f Docker/Gradio.Dockerfile . -t bigcodebench/bigcodebench-gradio:$version
docker tag bigcodebench/bigcodebench-gradio:$version bigcodebench/bigcodebench-gradio:latest
docker push bigcodebench/bigcodebench-gradio:$version
docker push bigcodebench/bigcodebench-gradio:latest