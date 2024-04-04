build:
	docker buildx build --platform linux/amd64,linux/arm64 -t funkaoshi/lotfp-summon:latest -t funkaoshi/lotfp-summon:1 --push .

run:
	docker run -p 8001:8001 -t lotfp-summon

push:
	docker push funkaoshi/lotfp-summon:latest

deploy:
	ssh ubuntu@oci.vqvz.com "cd oracle_free_vm/docker && docker-compose pull && docker-compose restart funkaoshi-lotfp-summon"
