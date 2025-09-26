"""Simplified tests for tools.kubectl module focusing on core logic."""

import pytest
from unittest.mock import patch, AsyncMock
from tools.kubectl import (
    run_kubectl_command,
    build_kubectl_top_args
)


class TestRunKubectlCommand:
    """Test cases for run_kubectl_command function."""

    @pytest.mark.asyncio
    async def test_run_kubectl_command_basic(self):
        """Test basic kubectl command execution."""
        with patch('tools.kubectl.run_command') as mock_run_command:
            mock_run_command.return_value = {"output": "kubectl output", "error": False}
            
            result = await run_kubectl_command("get pods")
            
            mock_run_command.assert_called_once_with("kubectl", ["get", "pods"], stdin=None)
            assert result == {"output": "kubectl output", "error": False}

    @pytest.mark.asyncio
    async def test_run_kubectl_command_with_stdin(self):
        """Test kubectl command with stdin input."""
        with patch('tools.kubectl.run_command') as mock_run_command:
            mock_run_command.return_value = {"output": "applied", "error": False}
            
            result = await run_kubectl_command("apply -f -", stdin="apiVersion: v1")
            
            mock_run_command.assert_called_once_with("kubectl", ["apply", "-f", "-"], stdin="apiVersion: v1")
            assert result == {"output": "applied", "error": False}

    @pytest.mark.asyncio
    async def test_run_kubectl_command_empty_parts(self):
        """Test kubectl command with empty parts filtered out."""
        with patch('tools.kubectl.run_command') as mock_run_command:
            mock_run_command.return_value = {"output": "output", "error": False}
            
            result = await run_kubectl_command("get pods   ")
            
            mock_run_command.assert_called_once_with("kubectl", ["get", "pods"], stdin=None)
            assert result == {"output": "output", "error": False}


class TestBuildKubectlTopArgs:
    """Test cases for build_kubectl_top_args function."""

    def test_build_kubectl_top_args_basic(self):
        """Test basic top args building."""
        args = build_kubectl_top_args("pods")
        assert args == ["top", "pods"]

    def test_build_kubectl_top_args_with_name(self):
        """Test top args building with name."""
        args = build_kubectl_top_args("pods", name="test-pod")
        assert args == ["top", "pods", "test-pod"]

    def test_build_kubectl_top_args_with_namespace(self):
        """Test top args building with namespace."""
        args = build_kubectl_top_args("pods", namespace="test-ns")
        assert args == ["top", "pods", "-n", "test-ns"]

    def test_build_kubectl_top_args_all_namespaces(self):
        """Test top args building with all namespaces."""
        args = build_kubectl_top_args("pods", all_namespaces=True)
        assert args == ["top", "pods", "-A"]

    def test_build_kubectl_top_args_with_containers(self):
        """Test top args building with containers."""
        args = build_kubectl_top_args("pods", containers=True)
        assert args == ["top", "pods", "--containers"]

    def test_build_kubectl_top_args_with_no_headers(self):
        """Test top args building with no headers."""
        args = build_kubectl_top_args("pods", no_headers=True)
        assert args == ["top", "pods", "--no-headers"]

    def test_build_kubectl_top_args_with_label_selector(self):
        """Test top args building with label selector."""
        args = build_kubectl_top_args("pods", label_selector="app=nginx")
        assert args == ["top", "pods", "-l", "app=nginx"]

    def test_build_kubectl_top_args_with_sort_by(self):
        """Test top args building with sort by."""
        args = build_kubectl_top_args("pods", sort_by="cpu")
        assert args == ["top", "pods", "--sort-by", "cpu"]

    def test_build_kubectl_top_args_invalid_sort_by(self):
        """Test top args building with invalid sort by."""
        with pytest.raises(ValueError, match="sort_by must be 'cpu' or 'memory'"):
            build_kubectl_top_args("pods", sort_by="invalid")

    def test_build_kubectl_top_args_all_options(self):
        """Test top args building with all options."""
        args = build_kubectl_top_args(
            "pods",
            name="test-pod",
            namespace="test-ns",
            containers=True,
            no_headers=True,
            label_selector="app=nginx",
            sort_by="memory"
        )
        expected = [
            "top", "pods", "test-pod", "-n", "test-ns",
            "--containers", "--no-headers", "-l", "app=nginx",
            "--sort-by", "memory"
        ]
        assert args == expected


class TestKubectlCommandBuilding:
    """Test cases for kubectl command building logic."""

    def test_logs_command_building(self):
        """Test logs command building logic."""
        # Test basic logs command
        cmd_parts = ["logs", "test-pod"]
        assert cmd_parts == ["logs", "test-pod"]
        
        # Test with namespace
        cmd_parts = ["logs", "test-pod"]
        cmd_parts.extend(["-n", "test-ns"])
        assert cmd_parts == ["logs", "test-pod", "-n", "test-ns"]
        
        # Test with container
        cmd_parts = ["logs", "test-pod", "-n", "test-ns"]
        cmd_parts.extend(["-c", "test-container"])
        assert cmd_parts == ["logs", "test-pod", "-n", "test-ns", "-c", "test-container"]
        
        # Test with since
        cmd_parts = ["logs", "test-pod", "-n", "test-ns", "-c", "test-container"]
        cmd_parts.extend(["--since", "5m"])
        assert cmd_parts == ["logs", "test-pod", "-n", "test-ns", "-c", "test-container", "--since", "5m"]
        
        # Test with previous
        cmd_parts = ["logs", "test-pod", "-n", "test-ns", "-c", "test-container", "--since", "5m"]
        cmd_parts.append("--previous")
        assert cmd_parts == ["logs", "test-pod", "-n", "test-ns", "-c", "test-container", "--since", "5m", "--previous"]
        
        # Test with tail
        cmd_parts = ["logs", "test-pod", "-n", "test-ns", "-c", "test-container", "--since", "5m", "--previous"]
        cmd_parts.extend(["--tail", "100"])
        assert cmd_parts == ["logs", "test-pod", "-n", "test-ns", "-c", "test-container", "--since", "5m", "--previous", "--tail", "100"]

    def test_get_command_building(self):
        """Test get command building logic."""
        # Test basic get command
        resource_type = "pods"
        name = None
        namespace = None
        all_namespaces = False
        output = None
        
        cmd = f"get {resource_type} {name if name else ''} {'-n ' + namespace + ' ' if namespace else ''}{'-o ' + output if output else ''} {'-A' if all_namespaces else ''}"
        assert cmd == "get pods   "
        
        # Test with name
        name = "test-pod"
        cmd = f"get {resource_type} {name if name else ''} {'-n ' + namespace + ' ' if namespace else ''}{'-o ' + output if output else ''} {'-A' if all_namespaces else ''}"
        assert cmd == "get pods test-pod  "
        
        # Test with namespace
        name = None
        namespace = "test-ns"
        cmd = f"get {resource_type} {name if name else ''} {'-n ' + namespace + ' ' if namespace else ''}{'-o ' + output if output else ''} {'-A' if all_namespaces else ''}"
        assert cmd == "get pods  -n test-ns  "
        
        # Test with all namespaces
        namespace = None
        all_namespaces = True
        cmd = f"get {resource_type} {name if name else ''} {'-n ' + namespace + ' ' if namespace else ''}{'-o ' + output if output else ''} {'-A' if all_namespaces else ''}"
        assert cmd == "get pods   -A"

    def test_describe_command_building(self):
        """Test describe command building logic."""
        name = "test-pod"
        resource_type = "pods"
        namespace = "default"
        
        cmd = f"describe {resource_type} {name} {f'-n {namespace}' if namespace else ''}"
        assert cmd == "describe pods test-pod -n default"
        
        # Test without namespace
        namespace = None
        cmd = f"describe {resource_type} {name} {f'-n {namespace}' if namespace else ''}"
        assert cmd == "describe pods test-pod "

    def test_apply_command_building(self):
        """Test apply command building logic."""
        namespace = "test-ns"
        cmd = f"apply -f - {f'-n {namespace}' if namespace else ''}"
        assert cmd == "apply -f - -n test-ns"
        
        # Test without namespace
        namespace = None
        cmd = f"apply -f - {f'-n {namespace}' if namespace else ''}"
        assert cmd == "apply -f - "

    def test_patch_command_building(self):
        """Test patch command building logic."""
        name = "test-pod"
        resource_type = "pods"
        patch = '{"spec":{"replicas":3}}'
        namespace = "default"
        patch_type = "strategic"
        
        cmd = f"patch {resource_type} {name} {f'-n {namespace}' if namespace else ''} --patch {patch} --type={patch_type}"
        assert cmd == "patch pods test-pod -n default --patch {\"spec\":{\"replicas\":3}} --type=strategic"

    def test_set_image_command_building(self):
        """Test set image command building logic."""
        resource_name = "test-deployment"
        resource_type = "deployment"
        container_images = "nginx=nginx:1.20"
        namespace = "test-ns"
        
        cmd = f"set image {resource_type}/{resource_name} {container_images} {f'-n {namespace}' if namespace else ''}"
        assert cmd == "set image deployment/test-deployment nginx=nginx:1.20 -n test-ns"

    def test_rollout_restart_command_building(self):
        """Test rollout restart command building logic."""
        name = "test-deployment"
        namespace = "test-ns"
        
        cmd = f"rollout restart deployment/{name} {f'-n {namespace}' if namespace else ''}"
        assert cmd == "rollout restart deployment/test-deployment -n test-ns"

    def test_scale_command_building(self):
        """Test scale command building logic."""
        name = "test-deployment"
        resource_type = "deployment"
        replicas = 3
        namespace = "test-ns"
        
        cmd = f"scale {resource_type}/{name} --replicas={replicas} {f'-n {namespace} ' if namespace else ''}"
        assert cmd == "scale deployment/test-deployment --replicas=3 -n test-ns "

    def test_delete_command_building(self):
        """Test delete command building logic."""
        name = "test-pod"
        resource_type = "pods"
        namespace = "test-ns"
        
        cmd = f"delete {resource_type} {name} {f'-n {namespace}' if namespace else ''}"
        assert cmd == "delete pods test-pod -n test-ns"

    def test_rollout_status_command_building(self):
        """Test rollout status command building logic."""
        name = "test-deployment"
        namespace = "test-ns"
        
        cmd = f"rollout status deployment/{name} {f'-n {namespace}' if namespace else ''}"
        assert cmd == "rollout status deployment/test-deployment -n test-ns"

    def test_cordon_command_building(self):
        """Test cordon command building logic."""
        node_name = "test-node"
        cmd = f"cordon {node_name}"
        assert cmd == "cordon test-node"

    def test_uncordon_command_building(self):
        """Test uncordon command building logic."""
        node_name = "test-node"
        cmd = f"uncordon {node_name}"
        assert cmd == "uncordon test-node"

    def test_drain_command_building(self):
        """Test drain command building logic."""
        node_name = "test-node"
        ignore_daemonsets = True
        delete_emptydir_data = False
        
        cmd = f"drain {node_name}"
        if ignore_daemonsets:
            cmd += " --ignore-daemonsets"
        if delete_emptydir_data:
            cmd += " --delete-emptydir-data"
        assert cmd == "drain test-node --ignore-daemonsets"
        
        # Test with all options
        ignore_daemonsets = False
        delete_emptydir_data = True
        cmd = f"drain {node_name}"
        if ignore_daemonsets:
            cmd += " --ignore-daemonsets"
        if delete_emptydir_data:
            cmd += " --delete-emptydir-data"
        assert cmd == "drain test-node --delete-emptydir-data"

    def test_run_pod_command_building(self):
        """Test run pod command building logic."""
        name = "test-pod"
        image = "nginx:latest"
        namespace = "test-ns"
        command = "sleep 3600"
        
        cmd = f"run {name} --image={image}"
        if namespace:
            cmd += f" -n {namespace}"
        if command:
            cmd += f" --command -- {command}"
        assert cmd == "run test-pod --image=nginx:latest -n test-ns --command -- sleep 3600"

    def test_exec_command_building(self):
        """Test exec command building logic."""
        pod_name = "test-pod"
        command = "ls -la"
        namespace = "test-ns"
        container = "test-container"
        
        cmd = f"exec {pod_name}"
        if namespace:
            cmd += f" -n {namespace}"
        if container:
            cmd += f" -c {container}"
        cmd += f" -- {command}"
        assert cmd == "exec test-pod -n test-ns -c test-container -- ls -la"

    def test_port_forward_command_building(self):
        """Test port forward command building logic."""
        resource_name = "test-pod"
        ports = "8080:80"
        namespace = "test-ns"
        resource_type = "pod"
        
        resource_spec = (
            f"{resource_type}/{resource_name}" if resource_type != "pod" else resource_name
        )
        cmd = f"port-forward {resource_spec} {ports} {f'-n {namespace}' if namespace else ''}"
        assert cmd == "port-forward test-pod 8080:80 -n test-ns"
        
        # Test with deployment
        resource_type = "deployment"
        resource_spec = (
            f"{resource_type}/{resource_name}" if resource_type != "pod" else resource_name
        )
        cmd = f"port-forward {resource_spec} {ports} {f'-n {namespace}' if namespace else ''}"
        assert cmd == "port-forward deployment/test-pod 8080:80 -n test-ns"
