<script data-exec-on-popstate>
$(function () {

    $(".backup-run").click(function() {
        var $btn = $(this);
        $btn.button('loading');

        NProgress.start();
        $.ajax({
            url: $btn.attr('href'),
            data : {
                _token: LA.token
            },
            method: 'POST',
            success: function (data){

                if (data.status) {
                    $('.output-box').removeClass('hide');
                    $('.output-box .output-body').html(data.message)
                }

                $btn.button('reset');
                NProgress.done();
            }
        });

        return false;
    });

    $(".backup-delete").click(function() {

        var $btn = $(this);

        $.ajax({
            url: $btn.attr('href'),
            data : {
                _token: LA.token
            },
            method: 'DELETE',
            success: function (data){

                $.pjax.reload('#pjax-container');

                if (typeof data === 'object') {
                    if (data.status) {
                        toastr.success(data.message);
                    } else {
                        toastr.error(data.message);
                    }
                }

                $btn.button('reset');
            }
        });

        return false;
    });

});
</script>

<style>
    .output-body {
        white-space: pre-wrap;
        background: #000000;
        color: #00fa4a;
        padding: 10px;
        border-radius: 0;
    }

    .todo-list>li .tools {
        display: none;
        float: none;
        color: #3c8dbc;
        margin-left: 10px;
    }

</style>

<div class="box">
    <div class="box-header">
        <h3 class="box-title">Existing backups</h3>

        <div class="box-tools">
            <a href="<?php echo e(route('backup-run')); ?>" class="btn btn-dropbox backup-run">Backup</a>
        </div>
    </div>
    <!-- /.box-header -->
    <div class="box-body table-responsive no-padding">
        <table class="table table-hover">
            <tbody>
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Disk</th>
                <th>Reachable</th>
                <th>Healthy</th>
                <th># of backups</th>
                <th>Newest backup</th>
                <th>Used storage</th>
            </tr>
            <?php $__currentLoopData = $backups; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $index => $backup): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
            <tr data-toggle="collapse" data-target="#trace-<?php echo e($index+1); ?>" style="cursor: pointer;">
                <td><?php echo e($index+1); ?>.</td>
                <td><?php echo e($backup[0]); ?></td>
                <td><?php echo e($backup[1]); ?></td>
                <td><?php echo e($backup[2]); ?></td>
                <td><?php echo e($backup[3]); ?></td>
                <td><?php echo e($backup['amount']); ?></td>
                <td><?php echo e($backup['newest']); ?></td>
                <td><?php echo e($backup['usedStorage']); ?></td>
            </tr>
            <tr class="collapse" id="trace-<?php echo e($index+1); ?>">
                <td colspan="8">
                    <ul class="todo-list ui-sortable">
                        <?php $__currentLoopData = $backup['files']; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $file): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                        <li>
                            <span class="text"><?php echo e($file); ?></span>
                            <!-- Emphasis label -->

                            <div class="tools">
                                <a target="_blank" href="<?php echo e(route('backup-download', ['disk' => $backup[1], 'file' => $backup[0].'/'.$file])); ?>"><i class="fa fa-download"></i></a>
                                <a href="<?php echo e(route('backup-delete', ['disk' => $backup[1], 'file' => $backup[0].'/'.$file])); ?>" class="backup-delete"><i class="fa fa-trash-o"></i></a>
                            </div>
                        </li>
                        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                    </ul>
                </td>
            </tr>
            <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>

            </tbody>
        </table>
    </div>
    <!-- /.box-body -->
</div>

<div class="box box-default output-box hide">
    <div class="box-header with-border">
        <i class="fa fa-terminal"></i>

        <h3 class="box-title">Output</h3>
    </div>
    <!-- /.box-header -->
    <div class="box-body">
        <pre class="output-body"></pre>
    </div>
    <!-- /.box-body -->
</div>
