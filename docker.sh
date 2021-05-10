image=owen0222/aws-s3
version=v1.0.0

docker logout
docker login -u owen0222 -p
docker build --no-cache -t ${image}:${version} -t ${image}:latest .
docker push ${image}:${version}
docker push ${image}:latest
