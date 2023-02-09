#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import yaml
from time import sleep
from kubernetes  import client, config
from kubernetes.client.rest import ApiException


# DEFINES                                                                    
###############################################################################
CONFIG_FILE = "/home/eduardo/.kube/config"


# CLASSES                                                                    
###############################################################################
class Kubernetes:

    core_v1 = None
    apps_v1 = None
    
    def __init__(self, configFile):
        """      
        :param configFile: example: /home/eduardo/.kube/config
        """
        
        api_client = config.new_client_from_config(configFile)
        
        self.core_v1 = client.CoreV1Api(api_client)
        self.apps_v1 = client.AppsV1Api(api_client)


    def get_clusters(self):
        """
        Returns all clusters avalable the context files
        
        :return: all clusters
        """
        
        ## Get all clusters
        contexts, active_context = config.list_kube_config_contexts()
        
        if not contexts:
            print("Cannot find any context in kube-config file.")
            return
        
        return contexts
    
    
    def get_nodes(self):
        """
        Returns all node names available at the cluster
        
        :return: list of strings
        """
        allNodes = []
    
        ## Get all nodes:
        valRet = self.core_v1.list_node()
        
        for i in valRet.items:
            allNodes.append(i.metadata.name)
    
        return allNodes
        

    def get_endpoints(self):
        """
        Returns all active pods names
        
        :return: list of strings
        """
        
        allEndpoints = []
    
        ## Get all pods to all namespaces:
        valRet = self.core_v1.list_pod_for_all_namespaces(watch=False)
        
        for i in valRet.items:
            allEndpoints.append(i.metadata.name)

        return allEndpoints


    def create_deployment(self, filename: str, namespace: str):
        """
        Create deployment all active pods names
        
        :param filename: example: /etc/kubernetes/admin.conf
        :param name: example: mynamespace

        :return: resp
        """
        yamlDeploy = open(filename)
        jsonDeploy = yaml.safe_load(yamlDeploy)
        
        resp = None
        try:
            resp = self.apps_v1.create_namespaced_deployment(
                body=jsonDeploy,
                namespace=namespace
            )

            print("Deployment created. status='{}'".format(resp.metadata.name))
        except ApiException as e:
            print("Exception when calling create_deployment:\n{}".format(e))
        
        return resp

    
    def create_service(self, filename: str, namespace: str):
        """
        Create a service from the yaml file 
        
        :param filename: example: /etc/kubernetes/admin.conf
        :param name: example: mynamespace

        :return: resp
        """
        yamlService = open(filename)
        jsonService = yaml.safe_load(yamlService)
        
        resp = None
        try:
            resp = self.core_v1.create_namespaced_service(
                body=jsonService,
                namespace=namespace
            )

            print("Service created. status='{}'".format(resp.metadata.name))
        except ApiException as e:
            print("Exception when calling create_service:\n{}".format(e))
    
        return resp

    def delete_deployment(self, name: str, namespace: str):
        """
        Delete a deployment based on the name and namespace 
        
        :param name: example: simple-microservice
        :param namespace: example: mynamespace

        :return: resp
        """
        resp = None
        try:
            resp = self.apps_v1.delete_namespaced_deployment(
                body={},
                name=name,
                namespace=namespace
            )

            print("Deployment deleted. status='{}'".format(name))
        except ApiException as e:
            print("Exception when calling delete_deployment:\n{}".format(e))

        return resp


        """
        Delete a service based on the name and namespace 
        
        :param name: example: simple-microservice
        :param namespace: example: mynamespace

        :return: resp
        """
    def delete_service(self, name: str, namespace: str):
        resp = None
        try:
            resp = self.core_v1.delete_namespaced_service(
                body={},
                name=name,
                namespace=namespace
            )

            print("Service deleted. status='{}'".format(name))
        except ApiException as e:
            print("Exception when calling delete_service:\n{}".format(e))

        return resp
# END CLASS.


# TESTS
###############################################################################
def main():
    k8s = Kubernetes(CONFIG_FILE)

    # Testing get_clusters method
    clusters = k8s.get_clusters()
    print("Clusters:", clusters)

    # Testing get_nodes method
    nodes = k8s.get_nodes()
    print("Nodes:", nodes)

    # Testing get_endpoints method
    endpoints = k8s.get_endpoints()
    print("Endpoints:", endpoints)

    # Testing create_deployment method
    deployment_file = 'deployment.yaml'
    namespace = 'default'
    dep = k8s.create_deployment(deployment_file, namespace)

    # Testing create_service method
    service_file = 'service.yaml'
    namespace = 'default'
    svc = k8s.create_service(service_file, namespace)
    
    # Testing get_endpoints method again
    endpoints = k8s.get_endpoints()
    print("Endpoints:", endpoints)

    # Testing delete_deployment method
    name = dep.metadata.name
    namespace = 'default'
    k8s.delete_deployment(name, namespace)

    # Testing delete_service method
    name = svc.metadata.name
    namespace = 'default'
    k8s.delete_service(name, namespace)

    
if __name__ == '__main__':
    sys.exit(main())

# END TESTS.
